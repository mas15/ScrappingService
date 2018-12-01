import json

from base64 import b64encode
from nameko.rpc import RpcProxy, rpc
from nameko_redis import Redis

from entrypoints import ConflictError, NotFoundError, http
from scrapping import scrape_from_site
from utils import generate_id, read_scrapped_images, read_scrapped_text


class HttpService:
    name = "scrapping_api"
    scrapper = RpcProxy("scrapping_rpc_service")
    tasks = Redis('tasks_statuses')

    @http('POST', "/scrape")
    def scrape(self, request):
        url_to_scrape = request.get_data().decode()
        task_id = generate_id(url_to_scrape)
        if self.tasks.get(task_id):
            raise ConflictError(f'Task for {url_to_scrape} already exists')

        self.tasks.set(task_id, 'pending')
        self.scrapper.scrape_from_site.call_async(task_id, url_to_scrape)
        return task_id

    @http('GET', "/status/<task_id>")
    def check_status(self, request, task_id):
        status = self.tasks.get(task_id)
        if status is None:
            raise NotFoundError('There is no such a task')
        return status

    @rpc
    def set_status(self, task_id, status):
        self.tasks.set(task_id, status)

    @http('GET', "/get/<task_id>")
    def get_data(self, request, task_id):
        status = self.check_status(None, task_id)
        if status == 'pending':
            raise ConflictError("Task has not started to be processed yet")
        if status == 'processing':
            raise ConflictError("Url is processed now")

        text, images = read_scrapped_text(task_id), read_scrapped_images(task_id)
        encoded_images = [b64encode(img).decode('utf-8') for img in images]

        return json.dumps({
            'text': text,
            'images': encoded_images
        })


class ScrappingService:
    name = "scrapping_rpc_service"
    http_service = RpcProxy("scrapping_api")

    @rpc
    def scrape_from_site(self, task_id, url):
        self.http_service.set_status.call_async(task_id, 'processing')
        scrape_from_site(url, task_id)
        self.http_service.set_status.call_async(task_id, 'done')
