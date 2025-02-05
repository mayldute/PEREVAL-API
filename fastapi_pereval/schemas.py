from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    phone: str
    fam: str
    name: str
    otc: Optional[str] = None

    class Config:
        orm_mode = True


class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True


class CoordsBase(BaseModel):
    latitude: float
    longitude: float
    height: int

    class Config:
        orm_mode = True


class CoordsResponse(CoordsBase):
    id: int

    class Config:
        orm_mode = True


class PerevalAddedCreate(BaseModel):
    user_id: int
    coord_id: int
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    winter_level: Optional[str] = None
    summer_level: Optional[str] = None
    autumn_level: Optional[str] = None
    spring_level: Optional[str] = None

    class Config:
        orm_mode = True


class PerevalAddedResponse(PerevalAddedCreate):
    id: int
    date_added: datetime
    add_time: datetime
    status: str

    user: UserResponse
    coords: CoordsResponse
    images: List["PerevalImagesResponse"]

    class Config:
        orm_mode = True


class PerevalImagesCreate(BaseModel):
    pereval_id: int
    img_title: Optional[str] = None
    img: str

    class Config:
        orm_mode = True


class PerevalImagesResponse(PerevalImagesCreate):
    id: int

    class Config:
        orm_mode = True


class PerevalAreasCreate(BaseModel):
    id_parent: Optional[int] = None
    title: str

    class Config:
        orm_mode = True


class PerevalAreasResponse(PerevalAreasCreate):
    id: int

    class Config:
        orm_mode = True


class SprActivitiesTypesCreate(BaseModel):
    title: str

    class Config:
        orm_mode = True


class SprActivitiesTypesResponse(SprActivitiesTypesCreate):
    id: int

    class Config:
        orm_mode = True