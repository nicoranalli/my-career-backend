import os

from pydantic_settings import BaseSettings

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 1440))
    ALGORITHM: str = os.getenv('ALGORITHM', "HS256")
    FRONTEND_HOST: str = "http://localhost:5173"
    API_V1_STR: str = "/api/v1"

    MAIL_APP_PASSWORD: str = os.getenv('MAIL_APP_PASSWORD')
    DATABASE_URL: str = os.getenv('DB_URL')


""" 
    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')
 """
    

settings = Settings()

