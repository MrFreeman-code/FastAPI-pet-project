# Для чего писать тесты?
 
    - Тесты позволяют предотвращать попадание ошибок в продуктивную среду.
    - Они могут служить в качестве документации для кода.
    - Тесты способствуют улучшению архитектуры приложения.

## Типы тестов (Пирамида тестирования, снизу вверх):

    * Модульные тесты: Наибольшее количество тестов, которые выполняются последовательно. Они проверяют функциональность конкретного модуля (функции или метода).
    * Интеграционные тесты: Меньшее количество тестов, которые запускаются параллельно. Они проверяют взаимодействие между различными модулями.
    * Сквозные тесты: Ограниченное количество тестов, которые выполняют полное тестирование пользовательского пути (например, от регистрации до оформления заказа).
    * Ручное тестирование: Тестирование, выполняемое вручную, без автоматизации.

### Необходимые бибилиотеки для работы с Pytest указаны в `requirements.tests.txt`, а именно:
    
    - pytest;
    - pytest_check;
    - httpx.

#### Для написания тестов используем фреймворк Pytest:

    1) Создайте директорию `tests`, в которой будут храниться все модульные тесты.
    2) При создании модульного теста создайте файл с расширением `.py`, имя которого начинается с ключевого слова `test_`, за которым следует название модуля (функции или метода).
    3) В файле `test_module_name.py`, создайте тесты для роутов (endpoint), функций или классов. Все функции тестов должны начинаться с `test_`:

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

    4.1 Простой вариант: требует запуска web-сервера (соответственно, `main.py` должен быть запущен):
    
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

    4.2 Синхронное тестирование роута: несмотря на то, что в роуте используется асинхронная функция:

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

    4.3 Асинхронное тестирование роута:

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

#### Для запуска всех тестов, которые есть в директории `tests` создаем конфигурацию запуска для тестов:

    1) В меню Run и выбераем Edit Configurations.
    2) Далее `+` в верхнем левом углу и выбераем Python tests > pytest.
    3) Даем название в поле `Name` (например, "pytest ALL").
    4) Указываем тип конфигурации `Custom`.
    5) В поле `Working directory` укажаем путь к директории `tests`.