from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# FIXME: Hardcoded... how DB auth should be done?
DB_USER = "postgres"
DB_PASSWD = 12345
DB_HOSTNAME = "psql_database"
DB_NAME = "mydatabase"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_HOSTNAME}/{DB_NAME}"


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    bib_number = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __str__(self):
        return f"[{self.email}] [{self.bib_number}] [{self.image_path}]"

def get_images_by_bib_number(bib_number: int):
    session = SessionLocal()
    try:
        query_res = session.query(User).filter(User.bib_number == bib_number).all()
        return [user.image_path for user in query_res]
    finally:
        session.close()

def get_user_by_email(email: str):
    session = SessionLocal()
    try:
        return session.query(User).filter(User.email == email).first()
    finally:
        session.close()

def register_new_image(path: str, email: str, bib_number: int):
    session = SessionLocal()

    try:
        user = User(image_path=path, email=email, bib_number=bib_number)
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_user(image_path: str, email: str):
    session = SessionLocal()
    try:
        user = User(image_path=image_path, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_all_users():
    session = SessionLocal()
    try:
        return session.query(User).all()
    finally:
        session.close()

def delete_user(email: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user:
            session.delete(user)
            session.commit()
    finally:
        session.close()
