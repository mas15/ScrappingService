import pytest
from mock import MagicMock, Mock, patch
from nameko.testing.services import replace_dependencies, worker_factory

from service import HttpService, ScrappingService


@pytest.fixture()
def mock_save():
    with patch('scrapping.save_scrapped_text', Mock()) as mocked_save:
        yield mocked_save


@pytest.fixture()
def mock_http_service():
    return MagicMock()

@pytest.fixture()
def mock_scrapper_service():
    return MagicMock()

@pytest.fixture()
def mock_requests():
    mock_site = Mock()
    mock_site.text = "<html><head>some head</head><body>some text</body></html>"
    with patch('scrapping.requests', Mock()) as mocked_requests:
        mocked_requests.get = lambda url: mock_site
        yield mock_requests


@pytest.fixture()
def scrapping_service_worker(mock_save, mock_http_service, mock_requests):
    scrapping_service_worker = worker_factory(ScrappingService, http_service=mock_http_service)
    yield scrapping_service_worker


@pytest.fixture()
def api_service_container(container_factory, config, mock_redis, mock_scrapper_service):
    container = container_factory(HttpService, config)

    tasks_redis = mock_redis()
    tasks_redis.set('task_id_123', 'pending')

    replace_dependencies(container, scrapper=mock_scrapper_service)
    replace_dependencies(container, tasks=tasks_redis)

    container.start()
    yield container


@pytest.fixture()
def mock_redis():
    class Redis(object):
        def __init__(self):
            self._data = dict()

        def get(self, key):
            return self._data.get(key)

        def set(self, key, value):
            self._data[key] = value

    return Redis


@pytest.fixture()
def config(rabbit_config, web_config):
    config = rabbit_config
    config.update(web_config)
    return config
