import pytest
from mock import call
from nameko.testing.services import entrypoint_hook


@pytest.mark.parametrize("url, exp_code, exp_text", [
    ["/status/task_id_123", 200, 'pending'],
    ["/status/task_id_124", 404, '{"error": "NOT_FOUND", "message": "There is no such a task"}'],
])
def test_check_status(url, exp_code, exp_text, api_service_container, web_session):
    response = web_session.get(url)
    assert response.status_code == exp_code
    assert response.text == exp_text


def test_set_status(api_service_container, web_session):
    with entrypoint_hook(api_service_container, 'set_status') as set_status:
        set_status('task_id_123', 'done')
        set_status('task_id_125', 'processing')
        assert web_session.get("/status/task_id_123").text == 'done'
        assert web_session.get("/status/task_id_125").text == 'processing'


def test_get_data_when_there_is_no_task(api_service_container, web_session):
    response = web_session.get("/get/task_id_111")
    assert response.status_code == 404
    assert response.text == '{"error": "NOT_FOUND", "message": "There is no such a task"}'


def test_get_data_when_task_is_not_done(api_service_container, web_session):
    result = web_session.get("/get/task_id_123").text
    assert result == '{"error": "BAD_REQUEST", "message": "Task has not started to be processed yet"}'
    with entrypoint_hook(api_service_container, 'set_status') as set_status:
        set_status('task_id_123', 'processing')
        result = web_session.get("/get/task_id_123").text
        assert result == '{"error": "BAD_REQUEST", "message": "Url is processed now"}'

def test_get_data(api_service_container, web_session):
    pass

def test_scrap(api_service_container, web_session, mock_scrapper_service):
    reponse = web_session.post("/scrape", data='http://www.google.pl')
    assert reponse.status_code == 200
    task_id = reponse.text
    mock_scrapper_service.scrape_from_site.call_async.assert_called_with(task_id, 'http://www.google.pl')
    assert web_session.get(f"/status/{task_id}").text == 'pending'


def test_scrap_same_url_twice(api_service_container, web_session, mock_scrapper_service):
    web_session.post("/scrape", data='http://www.google.pl')
    reponse = web_session.post("/scrape", data='http://www.google.pl')
    assert reponse.status_code == 409
    assert reponse.text == '{"error": "BAD_REQUEST", "message": "Task for http://www.google.pl already exists"}'


def test_scrape_text(scrapping_service_worker, mock_save, mock_http_service):
    scrapping_service_worker.scrape_from_site("task_id_123", "http://www.google.pl")

    expected_calls = [
        call('task_id_123', 'processing'),
        call('task_id_123', 'done')
    ]
    mock_http_service.set_status.call_async.assert_has_calls(expected_calls)
    mock_save.assert_called_with("some text", "task_id_123")
