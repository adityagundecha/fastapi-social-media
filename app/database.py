from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils import get_db_url


# Connect to the db
# while True:
#     try:
#         conn = psycopg2.connect(host=HOST, database=DATABASE,
#                                 user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('DB Conn was successfull!')
#         break
#     except Exception as error:
#         print(f"Error: {error}")
#         time.sleep(2)

SQLALCHEMY_DATABASE_URL = get_db_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db()
