from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


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