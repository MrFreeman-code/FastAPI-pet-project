import pytest
from api.app import app
from fastapi import status
from fastapi.testclient import TestClient
import requests


@pytest.fixture()
def client():
    """Экземпляр pytest"""
    client = TestClient(app)
    return client


def test_add_one_task(client: TestClient):

    task_name = 'af'
    task_description = 'country'

    headers = {'accept': 'application/json'}

    # url = f'http://127.0.0.1:8080/task/add?name={task_name}&description={task_description}'
    url = 'http://127.0.0.1:8080/tasks/add?name=sex&description=s'
    response = requests.post(url, headers=headers)

    # url = f'/task/add?name={task_name}&description={task_description}'
    #response = client.post(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK


def test_get_all_tasks(client: TestClient):

    headers = {'accept': 'application/json'}

    # url = f'/tasks/get-all'
    # response = client.get(url, headers=headers)

    url = f'http://127.0.0.1:8080/tasks/get-all'
    response = requests.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK