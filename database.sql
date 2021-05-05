database: pethotel

CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    petname text,
    owner text
);

CREATE TABLE owners (
    id SERIAL PRIMARY KEY,
    name text
);
