from sqlalchemy.orm import Session
from . import models, schemas


class DatabaseService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: schemas.UserCreate):
        """Create a new user in the database"""
        db_user = models.User(**user_data.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def create_coords(self, coords_data: schemas.CoordsCreate):
        """Create a new coords in the database"""
        db_coords = models.Coords(**coords_data.model_dump())
        self.db.add(db_coords)
        self.db.commit()
        self.db.refresh(db_coords)
        return db_coords
    
    def create_pereval(self, pereval_data: schemas.PerevalAddedCreate, user_id: int, coords_id: int):
        """Create a new pereval_added in the database"""
        db_pereval_added = models.PerevalAdded(
            user_id=user_id,  
            coord_id=coords_id,
            beauty_title = pereval_data.beauty_title,
            title = pereval_data.title,
            other_titles = pereval_data.other_titles,
            connect = pereval_data.connect,
            add_time = pereval_data.add_time,
            winter_level = pereval_data.winter_level,
            summer_level = pereval_data.summer_level,
            autumn_level = pereval_data.autumn_level,
            spring_level = pereval_data.spring_level,
            status = 'new',
        )

        self.db.add(db_pereval_added)
        self.db.commit()
        self.db.refresh(db_pereval_added)
        return db_pereval_added
    
    def create_pereval_images(self, pereval_images_data: schemas.PerevalImagesCreate):
        """Create a new pereval_images in the database"""
        db_pereval_images = models.PerevalImages(
            pereval_id = pereval_images_data.pereval_id,
            img_title = pereval_images_data.img_title,
            img = pereval_images_data.img,
        )
        self.db.add(db_pereval_images)
        self.db.commit()
        self.db.refresh(db_pereval_images)
        return db_pereval_images
    
    def get_user_by_email(self, email: str):
        """Get a user by email"""
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get_pereval_by_id(self, pereval_id: int):
        """Get a pereval by id"""
        return self.db.query(models.PerevalAdded).filter(models.PerevalAdded.id == pereval_id).first()
    
    def get_pereval_by_email(self, user_email: str):
        """Get a perevals by email"""
        user = self.db.query(models.User).filter(models.User.email == user_email).first()
        if user:
            perevals = self.db.query(models.PerevalAdded).filter(models.PerevalAdded.user_id == user.id).all()
            return perevals
        return None