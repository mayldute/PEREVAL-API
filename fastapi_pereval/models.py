from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    fam = Column(String, nullable=False)
    name = Column(String, nullable=False)
    otc = Column(String, nullable=True)

    perevals = relationship("PerevalAdded", back_populates="user")


class Coords(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)


class PerevalAdded(Base):
    __tablename__ = "pereval_added"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    coord_id = Column(Integer, ForeignKey("coords.id"))

    beauty_title = Column(String, nullable=True)
    title = Column(String, nullable=False)
    other_titles = Column(String, nullable=True)
    connect = Column(String, nullable=True)
    add_time = Column(TIMESTAMP, default=func.now())

    winter_level = Column(String, nullable=True)
    summer_level = Column(String, nullable=True)
    autumn_level = Column(String, nullable=True)
    spring_level = Column(String, nullable=True)

    status = Column(String, default="new")  # new | pending | accepted | rejected

    user = relationship("User", back_populates="perevals")
    coords = relationship("Coords")
    images = relationship("PerevalImages", back_populates="pereval")


class PerevalImages(Base):
    __tablename__ = "pereval_images"

    id = Column(Integer, primary_key=True, index=True)
    pereval_id = Column(Integer, ForeignKey("pereval_added.id"))
    img_title = Column(String, nullable=True)  
    img = Column(String, nullable=False)  

    pereval = relationship("PerevalAdded", back_populates="images")


class PerevalAreas(Base):
    __tablename__ = "pereval_areas"

    id = Column(Integer, primary_key=True, index=True)
    id_parent = Column(Integer, nullable=True)
    title = Column(String, nullable=False)


class SprActivitiesTypes(Base):
    __tablename__ = "spr_activities_types"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)