Voici les commandes cURL pour tester les endpoints de user, amenities, reviews, et places sur une seule ligne :

1. User Endpoints

# Créer un nouvel utilisateur :

curl -X POST http://localhost:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'

# Récupérer tous les utilisateurs :

curl -X GET http://localhost:5000/api/v1/users/ -H "Content-Type: application/json"

# Récupérer les détails d'un utilisateur par ID :
# Remplacer le <user_id> par celui précedement crée

curl -X GET http://localhost:5000/api/v1/users/<user_id> -H "Content-Type: application/json"

# Mettre à jour un utilisateur par ID :
# Remplacer le <user_id> par celui précedement crée

curl -X PUT http://localhost:5000/api/v1/users/<user_id> -H "Content-Type: application/json" -d '{"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com"}'

2. Amenities Endpoints

# Créer une nouvelle commodité (amenity) :

curl -X POST http://localhost:5000/api/v1/amenities/ -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}'

# Récupérer toutes les commodités :

curl -X GET http://localhost:5000/api/v1/amenities/ -H "Content-Type: application/json"

# Récupérer une commodité par ID :
# Remplacer le <amenity_id> par celui précedement crée

curl -X GET http://localhost:5000/api/v1/amenities/<amenity_id> -H "Content-Type: application/json"

# Mettre à jour une commodité par ID :
# Remplacer le <amenity_id> par celui précedement crée

curl -X PUT http://localhost:5000/api/v1/amenities/<amenity_id> -H "Content-Type: application/json" -d '{"name": "Air Conditioning"}'

3. Places Endpoints

# Créer un nouveau lieu (place) :
# Remplacer le <owner_id> par celui précedement crée
# Remplacer le <amenity_id> par celui précedement crée

curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "owner_id": ["owner_id"], "amenities": ["amenity_id"]}'

# Récupérer tous les lieux :

curl -X GET http://localhost:5000/api/v1/places/ -H "Content-Type: application/json"

# Récupérer un lieu par ID :
# Remplacer le <place_id> par celui précedement crée

curl -X GET http://localhost:5000/api/v1/places/<place_id> -H "Content-Type: application/json"

# Mettre à jour un lieu par ID :
# Remplacer le <place_id> par celui précedement crée

curl -X PUT http://localhost:5000/api/v1/places/<place_id> -H "Content-Type: application/json" -d '{"title": "Luxury Condo", "description": "An upscale place to stay", "price": 200.0}'

4. Reviews Endpoints

# Créer un nouvel avis (review) :
# Remplacer le "user_id" par celui précedement crée
# Remplacer le "place_id" par celui précedement crée

curl -X POST http://localhost:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text": "Great place!", "rating": 5, "place_id": "d9885675-6687-4bd5-8c61-2b604b6fe30d", "user_id": "12345"}'

# Récupérer tous les avis :

curl -X GET http://localhost:5000/api/v1/reviews/ -H "Content-Type: application/json"

# Récupérer un avis par ID :
# Remplacer le <review_id> par celui précedement crée

curl -X GET http://localhost:5000/api/v1/reviews/<review_id> -H "Content-Type: application/json"

# Mettre à jour un avis par ID :
# Remplacer le <review_id> par celui précedement crée

curl -X PUT http://localhost:5000/api/v1/reviews/<review_id> -H "Content-Type: application/json" -d '{"text": "Amazing place!", "rating": 4}'
