# Импортируем из библиотеки (sqlalchemy) для работы с реляционными БД
# с расширением (ext) асинхронного (asyncio) "движка" create_async_engine
# и async_sessionmaker - "фабрика" создания сессий, по своей сути это открытие транзакций для работы с БД
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.db.sqlite.tables.task import Base
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker

# Создаем сам асинхронный движок:
# Для этого указывем URL БД (или адрес), который состоит из:
# названия БД (sqlite), драйвера (aiosqlite), название "файлика" самой БД в самом простом виде
engine = create_async_engine("sqlite+aiosqlite:///tasks.db")

# Создаем сессию к БД. Новый асинхронный сеанс (session) для работы с БД
# new_session = async_sessionmaker(engine, expire_on_commit=False)


# Создаем асинхронный sessionmaker
async_sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    """Асинхронный контекстный менеджер для получения сессии."""
    async with async_sessionmaker() as session:
        yield session

# Функция для создания таблиц асинхронно, тк используем асинхронный драйвер aiosqlite
async def create_tables():
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-core
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для удаления таблиц асинхронно, тк используем асинхронный драйвер aiosqlite
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)