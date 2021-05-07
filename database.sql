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

SELECT owners.name, COUNT(*) FROM pets 
JOIN owners ON pets.owner = owners.id
GROUP BY owners.name