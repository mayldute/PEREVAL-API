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


class CoordsCreate(BaseModel):
    latitude: float
    longitude: float
    height: int

    class Config:
        orm_mode = True


class CoordsResponse(CoordsCreate):
    id: int

    class Config:
        orm_mode = True


class PerevalImagesCreate(BaseModel):
    pereval_id: Optional[int] = None
    img_title: Optional[str] = None
    img: str  

    class Config:
        orm_mode = True


class PerevalImagesResponse(PerevalImagesCreate):
    id: int

    class Config:
        orm_mode = True


class PerevalAddedCreate(BaseModel):
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    user: UserCreate
    coords: CoordsCreate
    winter_level: Optional[str] = None
    summer_level: Optional[str] = None
    autumn_level: Optional[str] = None
    spring_level: Optional[str] = None

    images: List[PerevalImagesCreate] = []

    class Config:
        orm_mode = True


class PerevalAddedResponse(PerevalAddedCreate):
    id: int
    date_added: datetime
    add_time: datetime
    status: str

    user: UserResponse
    coords: CoordsResponse
    images: List[PerevalImagesResponse]

    class Config:
        orm_mode = True
