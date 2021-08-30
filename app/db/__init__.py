from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base_class import Base
import db.models
from core import APP_SETTINGS

engine = create_engine(APP_SETTINGS.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
CreateSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
