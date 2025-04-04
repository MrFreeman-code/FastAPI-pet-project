# Для чего писать тесты?
 
    - Тесты позволяют не выносить баги на продакшн;
    - Могут служить в роли документации;
    - Улучшают архитектуру приложения.

## Типы тестов (Пирамида тестирования, снизу вверх):
    |    
    |
    \/
    * Модульные тесты (таких тестов больше всего и запускаются они последовательно, проверяют работу конкретного модуля (функции или метода));
    * Интеграционные тесты (таких тестов меньше запускаются они параллельно); ?
    * Сквозные тесты (совсем не много, End-to-end, тестируют весь пользоваетельский путь (условно говоря от регистрации до наполнения корзины и оформления заказа);
    * Ручное тестирования (QI).

### Необходимые бибилиотеки для работы с Pytest указаны в `requirements.tests.txt`, а именно:
    
    - pytest;
    - pytest_check;
    - httpx.

#### Для написания тестов используем фреймворк Pytest:

    1) Создаем директорию tests, где будут находится все модульные тесты;
    2) При создании модульного теста создаем файл `.py`, где в начале указывается ключевое слово `test_`, а после название модуля (функции или метода);
    3) В самом файле `test_module_name.py`, создаются тесты для (роутов (endpoint), функций или классов);
        - Аналогичным образом, все функиции тестов начинаются с test:
            ````def test_foo():
                    ... 
                    assert foo() == True```
    4) Есть несколько вариатнтов тестирования, рассмотрим сам тестируемый роут:
   
     ```
    from fastapi import APIRouter
    
    router = APIRouter(prefix="/tasks", tags=["Tasks"])

    @router.get("/rout-for-tests", summary="Роут для тестирования разными способами!")
    async def rout_for_tests(
    ) -> list:
        tasks = []
        return tasks
    ```

    4.1 Самый примитивный вариант, требует запуска сервера (соответсвенно main.py должен быть запущен):
    
    ```
    import pytest
    import requests
    from fastapi import status

    def test_rout_for_tests():
        """Самый приметивный способ"""
        headers = {'accept': 'application/json'}
    
        url = f'http://127.0.0.1:8080/tasks/rout-for-tests'
        response = requests.get(url, headers=headers)
    
        assert response.status_code == status.HTTP_200_OK
    ``` 

    4.2 Вариант с синхронным тестированием роута, несмотря на то, что в самом роуте используется async функция:

    ```
    import pytest
    from api.app import app
    from fastapi import status
    from fastapi.testclient import TestClient

    @pytest.fixture()
    def client():
        """Экземпляр pytest"""
        client = TestClient(app)
        return client
    
    
    def test_rout_for_tests_sync(client: TestClient):
        """Используя TestClient, не требует запуска main.py"""
        headers = {'accept': 'application/json'}
    
        url = '/tasks/rout-for-tests'
        response = client.get(url, headers=headers)
    
        assert response.status_code == status.HTTP_200_OK
    ```

    4.3 Вариант с aсинхронным тестированием роута, в самом роуте используется async функция:

    ```
    import pytest
    from api.app import app
    from fastapi import status
    from httpx import AsyncClient, ASGITransport

    @pytest.mark.asyncio
    async def test_rout_for_tests_async():
        """ Вариант с асинхронным тестированием роута, в самом роуте используется async функция"""
        """Используя AsyncClient, не требует запуска main.py"""
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            headers = {'accept': 'application/json'}
    
            url = '/tasks/rout-for-tests'
            response = await ac.get(url, headers=headers)
    
            assert response.status_code == status.HTTP_200_OK
    ```