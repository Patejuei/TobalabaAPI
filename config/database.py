import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))


class Base(DeclarativeBase):
    pass


def create_tables():
    Base.metadata.create_all(engine)
