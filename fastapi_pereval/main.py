from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .services import DatabaseService
from .schemas import PerevalAddedCreate, PerevalImagesCreate, PerevalAddedResponse
from .models import Coords, PerevalImages

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/submitData")
async def submit_data(pereval_data: PerevalAddedCreate, db: Session = Depends(get_db)):
    try:
        db_service = DatabaseService(db)

        user = db_service.create_user(pereval_data.user)
        coords = db_service.create_coords(pereval_data.coords)
        
        pereval = db_service.create_pereval(
            pereval_data=pereval_data, 
            user_id=user.id,  
            coords_id=coords.id  
        )
        
        if pereval_data.images:
            for image_data in pereval_data.images:
                image_dict = image_data.dict()  
                image_dict["pereval_id"] = pereval.id
                db_service.create_pereval_images(PerevalImagesCreate(**image_dict))
        
        return {
            "status": 200,
            "message": "Перевал успешно создан",
            "id": pereval.id
        }

    except Exception as e:
        return {
            "status": 500,
            "message": f"Ошибка при выполнении операции: {str(e)}",
            "id": None
        }

@app.get("/submitData/{id}", response_model=PerevalAddedResponse)
async def get_pereval(id: int, db: Session = Depends(get_db)):
    try:
        db_service = DatabaseService(db)

        pereval = db_service.get_pereval_by_id(id)
        
        if not pereval:
            print(f"Перевал с ID {id} не найден")
            return {
                "status": 404,
                "message": f"Перевал с ID {id} не найден",
                "id": None
            }
        return pereval

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {str(e)}")
        return {
            "status": 500,
            "message": f"Ошибка при выполнении операции: {str(e)}",
            "id": None
        }
    
@app.patch("/submitData/{id}")
async def update_pereval(id: int, pereval_data: PerevalAddedCreate, db: Session = Depends(get_db)):
    try:
        db_service = DatabaseService(db)

        db_pereval = db_service.get_pereval_by_id(id)
        
        if not db_pereval:
            return {
                "state": 0,
                "message": f"Перевал с ID {id} не найден",
            }

        if db_pereval.status != "new":
            return {
                "state": 0,
                "message": "Перевал в статусе не 'new', редактировать нельзя.",
            }

        if pereval_data.title is not None:
            db_pereval.title = pereval_data.title
        if pereval_data.beauty_title is not None:
            db_pereval.beauty_title = pereval_data.beauty_title
        if pereval_data.other_titles is not None:
            db_pereval.other_titles = pereval_data.other_titles
        if pereval_data.connect is not None:
            db_pereval.connect = pereval_data.connect
        if pereval_data.add_time is not None:
            db_pereval.add_time = pereval_data.add_time
        if pereval_data.winter_level is not None:
            db_pereval.winter_level = pereval_data.winter_level
        if pereval_data.summer_level is not None:
            db_pereval.summer_level = pereval_data.summer_level
        if pereval_data.autumn_level is not None:
            db_pereval.autumn_level = pereval_data.autumn_level
        if pereval_data.spring_level is not None:
            db_pereval.spring_level = pereval_data.spring_level

        if pereval_data.coords is not None:
            coords = db.query(Coords).filter(Coords.id == db_pereval.coord_id).first()

            coords.latitude = pereval_data.coords.latitude
            coords.longitude = pereval_data.coords.longitude
            coords.height = pereval_data.coords.height

            db.commit()


        if pereval_data.images is not None:
            db.query(PerevalImages).filter(PerevalImages.pereval_id == id).delete()
            db.commit()

            for image_data in pereval_data.images:
                new_image = PerevalImages(
                    pereval_id=id,
                    img_title=image_data.img_title,
                    img=image_data.img,
                )
                db.add(new_image)


        db.commit()
    

        return {
            "state": 1,
            "message": "Перевал успешно отредактирован",
        }

    except Exception as e:
        return {
            "state": 0,
            "message": f"Ошибка при обновлении перевала: {str(e)}",
        }