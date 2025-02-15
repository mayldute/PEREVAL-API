from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

DB_HOST = os.getenv("FSTR_DB_HOST")
DB_PORT = os.getenv("FSTR_DB_PORT")
DB_LOGIN = os.getenv("FSTR_DB_LOGIN")
DB_PASS = os.getenv("FSTR_DB_PASS")
DB_NAME = os.getenv("FSTR_DB_NAME")

DATABASE_URL = f"postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()