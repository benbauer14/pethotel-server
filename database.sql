database: pethotel

CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    pet text,
    breed text,
    color text,
    checkedin boolean,
    owner integer REFERENCES owners(id)
);

CREATE TABLE owners (
    id SERIAL PRIMARY KEY,
    name text
);
