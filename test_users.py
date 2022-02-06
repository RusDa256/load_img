import datetime
from random import randint
import models, crud, schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./db_for_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

models.Base.metadata.create_all(bind=engine) 


def test_Open_Check_Delete():
    img = schemas.Image
    img_test = open("мост.jpg")

    db = SessionLocal()

    img.code = randint(1,42)
    img.name = img_test.name
    img.data = datetime.datetime.now()

    crud.create_image(db=db, image=img)

    img_from_db = crud.get_image(db=db, code=img.code)
    assert img_from_db.name == img.name 
    assert img_from_db.data == img.data.strftime("%Y-%m-%d %H:%M:%S.%f")

    crud.delete(db=db,code=img.code)