import os
import IPython
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path


DB_USER = "postgres"
DB_PASSWD = 12345
DB_HOSTNAME = "psql_database"
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
            file_paths.append("/".join(f.split("/")[-2:]))

    return file_paths


# Insert into PostgreSQL
def insert_file_paths(file_paths, chunk_size=100):
    session = SessionLocal() # opens session

    try:
        for i in range(0, len(file_paths), chunk_size):
            batch = file_paths[i:i + chunk_size]
            # Prepare data for bulk insert
            session.bulk_save_objects([DatasetFile(file_path=fp) for fp in batch])
            session.commit()  # Commit each batch
            print(f"Inserted {len(batch)} records.")
    except Exception as e:
        session.rollback()


if __name__ == "__main__":
    files = get_dataset_files()

    IPython.embed()

    # Run the script
    #file_paths = get_all_files(DIRECTORY_PATH)
    #insert_file_paths(file_paths)

    # Cleanup
    #cur.close()
    #conn.close()
