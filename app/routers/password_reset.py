from fastapi import APIRouter, Depends, HTTPException,status
from app import database, models, oauth2, send_email, utils
from sqlalchemy.orm import Session
from app.schema import password_reset_schema,password_update_schema

router = APIRouter(prefix="/password", tags=["Password Reset"])

@router.post("/",response_description="Password Reset", status_code=status.HTTP_201_CREATED)
async def password_reset(user_email:password_reset_schema.PasswordReset, db: Session = Depends(database.get_db)):
    email = user_email.dict()
    user = db.query(models.User).filter(models.User.email == email["email"]).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User does not exist")

    access_token = oauth2.create_access_token(data={"user_id":user.id})
    reset_link = f"http://localhost:8000/?access_token={access_token}"
    user_name = str(user.email).split("@")[0]
    await send_email.send_reset_password_mail("Reset Password",email["email"],{
        "title":"Password Reset",
        "name":email["email"],
        "reset_link":reset_link
    })
    return {"access_token": access_token, "token_type":"bearer"}


@router.put("/reset", response_description="Password reset")
def password_upate(new_password:password_update_schema.PasswordUpdate ,db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()
    request_data = {k:v for k,v in new_password.dict().items() if v is not None}
    hashed_password = utils.hash(request_data["password"])
    user_query.update({"email":user.email,"password":hashed_password, "created_at":user.created_at},synchronize_session=False)
    db.commit()
    return {"message":"password updated successfully"}



