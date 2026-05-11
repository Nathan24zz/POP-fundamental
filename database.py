# Create database connection

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# config for dabatase in url format
db_url = "postgresql://postgres:Engineer1@localhost:5432/pop_basic"
# create the connection to the DB
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
