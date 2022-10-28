from fastapi import FastAPI
from . import models
from .routers import user,auth, notes,password_reset
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notebook App", version=0.1)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(password_reset.router)


@app.get("/")
def default():
    return {"message":"hello world"}