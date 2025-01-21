import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables

DSN = 'postgresql://postgres:postgres@localhost:5432/bookstore_db'

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

SESSION = sessionmaker(bind=engine)()