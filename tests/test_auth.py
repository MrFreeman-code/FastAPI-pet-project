import os
import pytest

from dotenv import load_dotenv

from api.app import app
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """Экземпляр pytest"""
    client = TestClient(app)
    return client


def test_user_my_failure(client: TestClient):
    """Тест проверки работы авторизации. В данныом случае, что пользователь не авторизован"""

    headers = {'accept': 'application/json'}
    url = '/users/me'
    resource = client.get(url, headers=headers)

    return resource.status_code == status.HTTP_401_UNAUTHORIZED


def test_token_success(client: TestClient):
    """Тест получения токена пользователя"""

    # Загружаем переменные окружения из .env файла
    load_dotenv()

    grant_type = os.getenv("grant_type")
    username = os.getenv("username")
    password = os.getenv("secret")
    client_id = os.getenv("string")
    client_secret = os.getenv("string")

    url = '/token'
    headers = {'accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = (f'grant_type={grant_type}&'
            f'username={username}&'
            f'password={password}&'
            f'client_id={client_id}&'
            f'client_secret={client_secret}')

    resource = client.post(url, headers=headers, data=data)

    return resource.status_code == status.HTTP_200_OK

