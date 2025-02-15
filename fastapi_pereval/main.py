from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .services import DatabaseService
from .schemas import PerevalAddedCreate, PerevalImagesCreate

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
