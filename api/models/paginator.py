from pydantic import BaseModel, Field
from fastapi import Depends
from typing import Annotated

# Найти часововй гайд по фулстеку wiev.js
# https://rutube.ru/video/1aed0d495ee4631f00d78929d669d25a/
# https://github.com/zhanymkanov/fastapi-best-practices
# wget -c --reject "*.mp4" --reject "*.iso" --reject "rockyou2024.zip" --reject "*.ova" --reject "WIFISLAX-CURRENT-PLASMA.zip" --reject "crackstation.txt.gz" --reject "Multiple Arcade Machine Emulator (MAME).zip" -r -k -l inf -p -P /media/kali/0189e0d4-a55f-4128-8fdf-a0454d8ce225 -E -nc https://elhacker.info


# По своей сути Depends - это инъекция зависимостей

class PaginatorParams(BaseModel):
    # Устанавливаем дефолтные параметры, для limit по дефолту 10, при этом 0 <= limit <= 100
    limit: int = Field(10, ge=0, le=50, discription="Кол-во элем на странице")
    offset: int = Field(0, discription="Смещение для пагинации")


PaginatorParamsDepends = Annotated[PaginatorParams, Depends(PaginatorParams)]