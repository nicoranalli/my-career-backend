from app.database.db import engine
from app.database.db import Base
from app.models.user import User

def init_db():
    Base.metadata.create_all(bind=engine)
