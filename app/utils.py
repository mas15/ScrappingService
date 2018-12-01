import os
import hashlib

DOWNLOAD_DIR = "download"


def generate_id(url):
    hashed_id = hashlib.md5(url.encode('utf-8'))
    return hashed_id.hexdigest()


def _scrapped_text_filename(task_id):
    return os.path.join(DOWNLOAD_DIR, task_id + ".txt")


def read_scrapped_text(task_id):
    with open(_scrapped_text_filename(task_id), 'r') as f:
        return f.read()


def save_scrapped_text(content, task_id):
    with open(_scrapped_text_filename(task_id), 'w') as f:
        f.write(content)


def _task_imgs_dir(task_id):
    return os.path.join(DOWNLOAD_DIR, task_id)


def read_scrapped_images(task_id):
    data_dir = _task_imgs_dir(task_id)
    if not os.path.exists(data_dir):
        return []
    images_paths = [os.path.join(data_dir, file_name) for file_name in os.listdir(data_dir)]
    images = []
    for image_path in images_paths:
        with open(image_path, 'rb') as f:
            images.append(f.read())
    return images


def make_dir_for_images(task_id):
    data_dir = _task_imgs_dir(task_id)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def save_scrapped_image(content, i, task_id, ext):
    with open(os.path.join(_task_imgs_dir(task_id), f"{i}{ext}"), 'wb') as f:
        f.write(content)
