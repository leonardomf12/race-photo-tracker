import os
import IPython
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from db_tables import Image


DB_USER = "postgres"
DB_PASSWD = 12345
DB_HOSTNAME = "localhost"
DB_NAME = "mydatabase"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_HOSTNAME}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

REPO_PATH = Path(__file__).resolve().parent.parent


# Function to extract file paths
def get_dataset_files():
    dataset_path = REPO_PATH / "DataService/dataset"

    file_paths = []
    for f in dataset_path.rglob("*"):
        if f.is_file():
            file_paths.append("/".join(str(f).split("/")[-2:]))

    return file_paths


# Insert into PostgreSQL
def insert_file_paths(image_paths, chunk_size=100):
    session = SessionLocal() # opens session

    try:
        for i in range(0, len(image_paths), chunk_size):
            chunk = image_paths[i:i + chunk_size]
            values = [Image(image_path=path) for path in chunk]

            session.add_all(values)
            session.flush()
            session.commit()

            session.expunge_all()

        print("Dataset inserted successfully")

    except Exception as e:
        session.rollback() # Reverts all changes in this transaction
        print(f"\nError uploading image_paths: \n{e}")
    finally:
        session.close()


if __name__ == "__main__":
    files = get_dataset_files()
    insert_file_paths(files)
