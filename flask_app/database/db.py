# Database connection and operations
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///flask_app/instance/vacancies.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:////home/jongreedy/ai_finder_work/vacancies.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

# Создание таблиц
Base.metadata.create_all(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()