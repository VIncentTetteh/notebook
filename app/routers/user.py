from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, send_email
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not found")
    return user
