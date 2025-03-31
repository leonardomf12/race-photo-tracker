-- Create the database only if it doesn't exist (not needed in Docker if using `POSTGRES_DB`)
-- CREATE DATABASE mydatabase;

-- Switch to the correct database (only needed if running outside Docker)
-- \c mydatabase;

-- Create the users table if it doesn’t exist
CREATE TABLE IF NOT EXISTS users (
    bib_number SERIAL PRIMARY KEY,
    image_path TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Insert dummy data
INSERT INTO users (bib_number, image_path, email) VALUES
(1, 'image1', 'alice@example.com'),
(2, 'image2', 'bob@example.com'),
(3, 'image3', 'charlie@example.com')
ON CONFLICT (email) DO NOTHING;  -- Avoid duplicate inserts
