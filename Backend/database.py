from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:Anish%40080503@localhost:5432/inventorymgmt"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)