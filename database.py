from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("db_url")

engine = create_engine(db_url)
session = sessionmaker(autoflush=False,autocommit = False,bind=engine)