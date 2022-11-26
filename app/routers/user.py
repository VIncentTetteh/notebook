from pathlib import Path
from fastapi import File, UploadFile, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, utils, send_email, oauth2
from app.database import get_db
from app.schema import user_create_schema,user_schema

router = APIRouter(prefix="/users", tags=["Users"])
BASE_DIR = Path(__file__).resolve().parent.parent

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
async def create_user(user: user_create_schema.UserCreate, db: Session = Depends(get_db)):
    user_exits = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exits:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail="user already exist")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user_name = str(new_user.email).split("@")[0]
    await send_email.send_registration_mail("Registration Successful", new_user.email, {
        "title": "Registration Successful",
        "name": user_name
    })
    return new_user


@router.get("/{id}", response_model=user_schema.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not found")
    return user

@router.put("/picture", response_model=user_schema.User)
def update_profile_picture(file:UploadFile = File(...), current_user:int = Depends(oauth2.get_current_user)):
    file_slice = file.filename.split(".")[0]
    file_name = f"{file_slice}_{current_user.id}.png"
    base_location = Path(BASE_DIR,"uploads")
    file_location = f"{base_location}\{file_name}"
    with open(file_location,"wb+") as file_object:
        file_object.write(file.file.read())
    return {"id":current_user.id,"email":current_user.email,"created_at":current_user.created_at,
    "profile_picture":file_location}
