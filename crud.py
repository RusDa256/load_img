from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy.orm.exc import NoResultFound


def create_image(db:Session, image: schemas.Image):
    db_image = models.Image(code=image.code, name=image.name, data=image.data)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_image(db:Session, code: int):
    return db.query(models.Image).filter(models.Image.code == code).first()


def delete(db:Session, code: int):
    try:
        db.query(models.Image).filter(models.Image.code == code).one()
    except NoResultFound:
        return 'Is not found'

    db.query(models.Image).filter(models.Image.code == code).delete()
    db.commit()
    return 'delete code: ', code
