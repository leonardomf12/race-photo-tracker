CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE races (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE user_race (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    race_id INTEGER REFERENCES races(id) ON DELETE CASCADE,
    bib_number INTEGER NOT NULL,
    PRIMARY KEY (user_id, race_id),
    UNIQUE (race_id, bib_number)
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    image_path TEXT NOT NULL
);

CREATE TABLE image_bibs (
    image_id INTEGER REFERENCES images(id) ON DELETE CASCADE,
    race_id INTEGER REFERENCES races(id) ON DELETE CASCADE,
    bib_number INTEGER NOT NULL,
    FOREIGN KEY (race_id, bib_number) REFERENCES user_race(race_id, bib_number) ON DELETE CASCADE,
    PRIMARY KEY (image_id, race_id, bib_number)
);