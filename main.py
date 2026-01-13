from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.init_db import init_db
from app.core.config import settings
from app.api.routes import auth, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix=f"/auth")
app.include_router(user.router, prefix=f"/user")
@app.get('/')
async def root():
    return {"message": "Hello World"}