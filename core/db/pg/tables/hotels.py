from core.db.pg.session import Base
from sqlalchemy import JSON, Column, Integer, String


class Hotels(Base):
    __tablename__ = "hotels"
    __table_args__ = {
        "schema": "public"
    }

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)