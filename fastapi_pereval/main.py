from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from . import database, services, schemas, models

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/submitData")
async def submit_data(pereval_data: schemas.PerevalAddedCreate, db: Session = Depends(get_db)):
    """Create a new pereval in the database"""
    try:
        db_service = services.DatabaseService(db)

        user = db_service.get_user_by_email(pereval_data.user.email)

        if not user:
            user = db_service.create_user(pereval_data.user)

        coords = db_service.create_coords(pereval_data.coords)
        
        pereval = db_service.create_pereval(
            pereval_data=pereval_data, 
            user_id=user.id,  
            coords_id=coords.id  
        )
        
        if pereval_data.images:
            for image_data in pereval_data.images:
                image_dict = image_data.model_dump()  
                image_dict["pereval_id"] = pereval.id
                db_service.create_pereval_images(schemas.PerevalImagesCreate(**image_dict))
        
        return {
            "status": 200,
            "message": "Pereval successfully created",
            "id": pereval.id
        }

    except Exception as e:
        return {
            "status": 500,
            "message": f"Error during operation: {str(e)}",
            "id": None
        }

@app.get("/submitData/{id}", response_model=schemas.PerevalAddedResponse)
async def get_pereval(id: int, db: Session = Depends(get_db)):
    """Get pereval by ID"""
    try:
        db_service = services.DatabaseService(db)

        pereval = db_service.get_pereval_by_id(id)
        
        if not pereval:
            return {
                "status": 404,
                "message": f"Pereval with ID {id} not found",
                "id": None
            }
        return pereval

    except Exception as e:
        print(f"Error during request execution: {str(e)}")
        return {
            "status": 500,
            "message": f"Error during operation: {str(e)}",
            "id": None
        }
    
@app.patch("/submitData/{id}")
async def update_pereval(id: int, pereval_data: schemas.PerevalAddedCreate, db: Session = Depends(get_db)):
    """Update pereval by ID"""
    try:
        db_service = services.DatabaseService(db)

        db_pereval = db_service.get_pereval_by_id(id)
        
        if not db_pereval:
            return {
                "state": 0,
                "message": f"Pereval with ID {id} not found",
            }

        if db_pereval.status != "new":
            return {
                "state": 0,
                "message": "Pereval is not in 'new' status, editing is not allowed.",
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
            coords = db.query(models.Coords).filter(models.Coords.id == db_pereval.coord_id).first()

            coords.latitude = pereval_data.coords.latitude
            coords.longitude = pereval_data.coords.longitude
            coords.height = pereval_data.coords.height

            db.commit()


        if pereval_data.images is not None:
            db.query(models.PerevalImages).filter(models.PerevalImages.pereval_id == id).delete()
            db.commit()

            for image_data in pereval_data.images:
                new_image = models.PerevalImages(
                    pereval_id=id,
                    img_title=image_data.img_title,
                    img=image_data.img,
                )
                db.add(new_image)


        db.commit()
    

        return {
            "state": 1,
            "message": "Pereval successfully updated",
        }

    except Exception as e:
        return {
            "state": 0,
            "message": f"Error updating pereval: {str(e)}",
        }
    
@app.get("/submitData/", response_model=List[schemas.PerevalAddedResponse])
async def get_pereval_by_user(user_email: str, db: Session = Depends(get_db)):
    """Get perevals by user email"""
    try:
        db_service = services.DatabaseService(db)
        perevals = db_service.get_pereval_by_email(user_email)

        if not perevals:
            return {
                "status": 404,
                "message": "Pereval not found",
                "user_email": user_email
            }

        return perevals  

    except Exception as e:
        return {
            "status": 500,
            "message": f"Error during operation: {str(e)}",
            "user_email": user_email
        }