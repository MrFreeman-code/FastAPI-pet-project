# Импортируем из библиотеки (sqlalchemy) для работы с реляционными БД
# с расширением (ext) асинхронного (asyncio) "движка" create_async_engine
# и async_sessionmaker - "фабрика" создания сессий, по своей сути это открытие транзакций для работы с БД
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


# Создаем сам асинхронный движок:
# Для этого указывем URL БД (или адрес), который состоит из:
# названия БД (sqlite), драйвера (aiosqlite), название "файлика" самой БД в самом простом виде
engine = create_async_engine("sqlite+aiosqlite:///tasks.db")

# Создаем сессию к БД. Новый асинхронный сеанс (session) для работы с БД
new_session = async_sessionmaker(engine, expire_on_commit=False)

# Теперь описываем класс Base, наследуемую от класса DeclarativeBase, от которой будут наследоваться уже все остальные классы (таблицы):
class Base(DeclarativeBase):
    pass

# Далее описываем саму таблицу (класс), наследуемую от класса Base, для этого:
class TaskTable(Base):
    __tablename__ = "tasks"

    # Описывем поле id и указываем, что оно PK. Обязательно нужен один PK, иначе SQLAlchemy не даст создать таблицу

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

# Функция для создания таблиц асинхронно, тк используем асинхронный драйвер aiosqlite
async def create_tables():
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-core
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для удаления таблиц асинхронно, тк используем асинхронный драйвер aiosqlite
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)