import bcrypt

password = "admin1234"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())

INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$D9yKk6X3H0JhFO6ycV0yWeOm1Od/jZMN2l5.8b1AIXF.JKwfFSkka',
    TRUE
);

INSERT INTO Amenity (id, name) VALUES
    ('1c4ad4fc-bf63-4cb6-9d57-1a0c4d1a1234', 'WiFi'),
    ('2a5d64fe-d6c7-4d80-98c3-0a7e4a7a2345', 'Piscine'),
    ('3b6e75ef-f5a8-498a-b893-1b8f7a8b3456', 'Climatisation');
