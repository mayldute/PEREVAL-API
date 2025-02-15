import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_pereval import models, schemas, services
from faker import Faker

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()

    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield db
    db.close()

@pytest.fixture
def db_service(db):
    return services.DatabaseService(db)

@pytest.fixture
def user_and_coords(db_service):
    fake = Faker()
    user_data = schemas.UserCreate(
        email=fake.email(),
        phone="+8 888 88 88",
        fam="testuser",
        name="testuser",
    )
    coords_data = schemas.CoordsCreate(latitude=40.7128, longitude=74.0060, height=5000)

    user = db_service.create_user(user_data)
    coords = db_service.create_coords(coords_data)
    return user, coords

@pytest.fixture
def pereval_data(user_and_coords):
    user, coords = user_and_coords
    return schemas.PerevalAddedCreate(
        beauty_title="Величественный Эверест",
        title="Пик Эверест",
        other_titles="Эверест, гора",
        connect="Местоположение",
        add_time="2025-02-15",
        user=user,
        coords=coords,
        winter_level="4",
        summer_level="5",
        autumn_level="3",
        spring_level="4",
    )

def test_create_user(user_and_coords):
    user, coords = user_and_coords

    assert user.email == user.email
    assert user.phone == user.phone
    assert user.fam == user.fam
    assert user.name == user.name


def test_create_coords(user_and_coords):
    user, coords = user_and_coords

    assert coords.latitude == 40.7128
    assert coords.longitude == 74.0060
    assert coords.height == 5000


def test_create_pereval(db_service, user_and_coords, pereval_data):
    user, coords = user_and_coords
    
    pereval = db_service.create_pereval(pereval_data, user.id, coords.id)

    assert pereval.title == "Пик Эверест"
    assert pereval.beauty_title == "Величественный Эверест"
    assert pereval.status == "new"
    assert pereval.user_id == user.id
    assert pereval.coord_id == coords.id


def test_create_pereval_images(db_service, user_and_coords, pereval_data):
    user, coords = user_and_coords
    
    pereval = db_service.create_pereval(pereval_data, user.id, coords.id)

    image_data = schemas.PerevalImagesCreate(pereval_id=pereval.id, img_title="Эверест изображение", img="image_data")
    image = db_service.create_pereval_images(image_data)

    assert image.pereval_id == pereval.id
    assert image.img_title == "Эверест изображение"
    assert image.img == "image_data"


def test_get_user_by_email(db_service, user_and_coords):
    user, coords = user_and_coords
    
    found_user = db_service.get_user_by_email(user.email)
    
    assert found_user.email == user.email


def test_get_pereval_by_id(db_service, user_and_coords, pereval_data):
    user, coords = user_and_coords
    
    pereval = db_service.create_pereval(pereval_data, user.id, coords.id)
    found_pereval = db_service.get_pereval_by_id(pereval.id)
    
    assert found_pereval.id == pereval.id


def test_get_pereval_by_email(db_service, user_and_coords, pereval_data):
    user, coords = user_and_coords
    
    db_service.create_pereval(pereval_data, user.id, coords.id)
    
    perevals = db_service.get_pereval_by_email(user.email)
    
    assert len(perevals) > 0
    assert perevals[0].title == "Пик Эверест"