from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from app import models,database
from app.routers import auth, user, notes, password_reset



models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Notebook App", version=0.1)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(password_reset.router)


handler = Mangum(app=app) 

@app.get("/")
def default():
    return {"message":"Welcome to the notebook app"}
