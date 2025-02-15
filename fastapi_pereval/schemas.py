from pydantic import BaseModel, EmailStr,  ConfigDict
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    fam: str
    name: str
    otc: Optional[str] = None

    class Config(ConfigDict): 
        from_attributes = True 

class UserResponse(UserCreate):
    id: int

    class Config(ConfigDict): 
        from_attributes = True 


class CoordsCreate(BaseModel):
    latitude: float
    longitude: float
    height: int

    class Config(ConfigDict): 
        from_attributes = True 


class CoordsResponse(CoordsCreate):
    id: int

    class Config(ConfigDict): 
        from_attributes = True 


class PerevalImagesCreate(BaseModel):
    pereval_id: Optional[int] = None
    img_title: Optional[str] = None
    img: str  

    class Config(ConfigDict): 
        from_attributes = True 


class PerevalImagesResponse(PerevalImagesCreate):
    id: int

    class Config(ConfigDict): 
        from_attributes = True 


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

    class Config(ConfigDict): 
        from_attributes = True 
        

class PerevalAddedResponse(PerevalAddedCreate):
    id: int
    add_time: datetime
    status: str

    title: str
    beauty_title: str
    other_titles: str
    connect: str
    winter_level: str
    summer_level: str
    autumn_level: str
    spring_level: str

    user: UserResponse
    coords: CoordsResponse
    images: List[PerevalImagesResponse]

    class Config(ConfigDict): 
        from_attributes = True 


