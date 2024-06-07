from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE = "postgresql://postgres:example@192.168.106.2:5432/db"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# def create_db_and_tables():
#     engine = create_engine(settings.db_url)
#     SQLModel.metadata.create_all(engine)
