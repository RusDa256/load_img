from fastapi import FastAPI, File, Query, UploadFile, Depends, HTTPException
import datetime
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models, schemas
from typing import List
from authorization import fake_users_db, UserInDB, fake_hash_password, get_current_active_user, User


models.Base.metadata.create_all(bind=engine) 
app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/get_img/")
async def read_item(code: int, db: Session = Depends(get_db)):
    return {crud.get_image(db=db, code=code)}


@app.post("/create_img/")
async def create_upload_file(
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db), 
    code: List[int]= Query(...)):

    img = schemas.Image
    j = 0

    for i in files:
        img.code = code[j]
        j = j + 1
        img.name = i.filename
        img.data = datetime.datetime.now()

        contents = await i.read()
        with open(i.filename, "wb") as f:
            f.write(contents)

        crud.create_image(db=db, image=img)

    return


@app.delete("/delete/")
def delete_hero(code: int, db: Session = Depends(get_db)):
    return crud.delete(db=db, code=code)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user