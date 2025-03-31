import pytest
import requests

from api.app import app

from fastapi import status
from fastapi.testclient import TestClient

from httpx import AsyncClient, ASGITransport


@pytest.fixture()
def client():
    """Экземпляр pytest"""
    client = TestClient(app)
    return client


def test_rout_for_tests_sync(client: TestClient):
    """ 1 вариант с синхронным тестированием роута, несмотря на то, что в самом роуте используется async функция"""
    """Используя TestClient, не требует запуска main.py"""
    headers = {'accept': 'application/json'}

    url = '/tasks/rout-for-tests'
    response = client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_rout_for_tests_async():
    """ 2 вариант с асинхронным тестированием роута, в самом роуте используется async функция"""
    """Используя AsyncClient, не требует запуска main.py"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        headers = {'accept': 'application/json'}

        url = '/tasks/rout-for-tests'
        response = await ac.get(url, headers=headers)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.xfail()
def test_rout_for_tests():
    """ 3 вариат, самый приметивный способ, требует запуска main.py"""
    headers = {'accept': 'application/json'}

    url = f'http://127.0.0.1:8080/tasks/rout-for-tests'
    response = requests.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK



# def test_add_one_task(client: TestClient):
#
#     task_name = 'af'
#     task_description = 'country'
#
#     headers = {'accept': 'application/json'}
#
#     url = f'http://127.0.0.1:8080/tasks/add?name={task_name}&description={task_description}'
#     response = requests.post(url, headers=headers)
#
#     # url = f'/tasks/add?name={task_name}&description={task_description}'
#     # response = client.post(url, headers=headers)
#
#     assert response.status_code == status.HTTP_200_OK


# def test_get_all_tasks(client: TestClient):
#
#     headers = {'accept': 'application/json'}
#
#     # url = f'http://127.0.0.1:8080/tasks/get-all'
#     # response = requests.get(url, headers=headers)
#
#     url = f'/tasks/get-all'
#     response = client.get(url, headers=headers)
#
#     assert response.status_code == status.HTTP_200_OK