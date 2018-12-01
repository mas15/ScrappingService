import mimetypes
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

from utils import make_dir_for_images, save_scrapped_image, save_scrapped_text


def scrape_from_site(url, task_id):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scrape_images(soup, url, task_id)
    scrape_text(soup, task_id)


def is_tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def scrape_text(soup, task_id):
    texts = soup.findAll(text=True)
    visible_texts = filter(is_tag_visible, texts)
    result = "\n".join(t.strip() for t in visible_texts)
    save_scrapped_text(result, task_id)


def scrape_images(soup, base_url, task_id):
    def _fix_relative_url(img_url):
        return urljoin(base_url, img_url) if 'http' not in img_url else img_url

    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags]
    img_urls = [_fix_relative_url(url) for url in img_urls]

    if img_urls:
        make_dir_for_images(task_id)
        for i, img_url in enumerate(img_urls):
            response = requests.get(img_url)
            content_type = response.headers['content-type']
            extension = mimetypes.guess_extension(content_type)

            save_scrapped_image(response.content, i, task_id, extension)
