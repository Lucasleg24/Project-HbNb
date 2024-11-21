CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) CHECK (price >= 0),
    latitude FLOAT CHECK (latitude BETWEEN -90 AND 90),
    longitude FLOAT CHECK (longitude BETWEEN -180 AND 180),
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);