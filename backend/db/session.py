import os
from urllib.parse import quote_plus

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.base import Base  # noqa: F401
from backend.doc_insighter.tools.app_logger import Logger

load_dotenv()
log = Logger()

DB_USER = os.getenv("user", "postgres")
DB_PASSWORD = os.getenv("password", "")
DB_HOST = os.getenv("host", "localhost")
DB_PORT = os.getenv("port", "5432")
DB_NAME = os.getenv("dbname", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=180,
    pool_size=5,
    max_overflow=2,
    pool_timeout=10,
    connect_args={"connect_timeout": 5},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        log.log_error(f"Error while connecting db- {e}")
        raise
    finally:
        log.log_debug(f"Closing DB Connection")
        db.close()


def test_connection():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
        )
        print("Connection successful!")
        cursor = connection.cursor()
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("Current Time:", result)
        cursor.close()
        connection.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Failed to connect: {e}")
