from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from fastapi_pereval.main import app 
from fastapi_pereval import schemas, models, services
from datetime import datetime

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
def client():
    return TestClient(app)

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
        add_time=datetime(2025, 2, 15),
        user=user,
        coords=coords,
        winter_level="4",
        summer_level="5",
        autumn_level="3",
        spring_level="4",
    )


def test_submit_data(client, pereval_data):
    data = pereval_data.dict()
    data["add_time"] = data["add_time"].isoformat()  
    response = client.post("/submitData", json=data)

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert "id" in response.json()


def test_get_pereval_by_id(client, pereval_data):
    data = pereval_data.dict()
    data["add_time"] = data["add_time"].isoformat()  
    response = client.post("/submitData", json=data)
    pereval_id = response.json()["id"]
    
    response = client.get(f"/submitData/{pereval_id}")
    
    assert response.status_code == 200
    assert response.json()["title"] == pereval_data.title
    assert response.json()["beauty_title"] == pereval_data.beauty_title


def test_update_pereval(client, pereval_data):
    data = pereval_data.dict()
    data["add_time"] = data["add_time"].isoformat()  
    response = client.post("/submitData", json=data)
    pereval_id = response.json()["id"]

    updated_data = pereval_data.dict()
    updated_data["title"] = "Новый Пик Эверест"
    updated_data["add_time"] = updated_data["add_time"].isoformat()  

    response = client.patch(f"/submitData/{pereval_id}", json=updated_data)

    assert response.status_code == 200
    assert response.json()["state"] == 1
    assert response.json()["message"] == "Pereval successfully updated"


def test_get_pereval_by_email(client, user_and_coords, pereval_data):
    user, coords = user_and_coords
    data = pereval_data.dict()
    data["add_time"] = data["add_time"].isoformat()  
    response = client.post("/submitData", json=data)
    
    response = client.get(f"/submitData/?user_email={user.email}")

    response_data = response.json()
    print(response_data)
    
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response_data[0]["user"]["email"] == user.email
