# 1.Run the server
# 2.Run the test file "python3 api.py"

import unittest
from unittest.mock import patch, Mock
import requests

API = "http://localhost:5000/api/v1"

def req(endpoint, methods="GET", payload=None):
    response = requests.request(
        methods,
        f"{API}/{endpoint}",
        headers={"Content-Type": "application/json"} if methods == "POST" or methods == "PUT" else None,
        json=payload if methods in ["POST", "PUT"] else None
    )

    if response.status_code == 500:
        print(f"Erreur 500 reçue : {response.text}")

    try:
        return response.json(), response.status_code
    except ValueError:
        return {"error": "Réponse non JSON", "content": response.text}, response.status_code

def post(endpoint, payload):
    return req(endpoint, "POST", payload)

def put(endpoint, payload):
    return req(endpoint, "PUT", payload)

def get(endpoint):
    return req(endpoint, "GET")


class TestUserEndpoint(unittest.TestCase):

    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    def test_create_user(self, mock_put, mock_get, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"
        })

        print("Testing POST /users with valid input")
        data, status = post("users", {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"})
        print(f"Expected: 201, Actual: {status}, Data: {data}")

        self.assertEqual(status, 201)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "john.doe@example.com")

        id = data["id"]

        mock_post.return_value = Mock(status_code=400, json=lambda: {
            "error": "Email already registered"
        })
        print("Testing POST /users with duplicate email")
        data, status = post("users", {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"})
        print(f"Expected: 400, Actual: {status}, Data: {data}")

        self.assertEqual(status, 400)
        self.assertEqual(data["error"], "Email already registered")

        mock_post.return_value = Mock(status_code=400, json=lambda: {
            "errors": {"email": "'email' is a required field"}
        })
        print("Testing POST /users with missing email field")
        data, status = post("users", {"first_name": "John"})
        print(f"Expected: 400, Actual: {status}, Data: {data}")

        self.assertEqual(status, 400)
        self.assertIn("'email' is a required", data["errors"]["email"])

        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "id": id, "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"
        })
        print(f"Testing GET /users/{id}")
        data, status = get(f"users/{id}")
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["first_name"], "John")

    @patch('requests.put')
    def test_update_user(self, mock_put):
        data, status = post("users", {"first_name": "John2", "last_name": "Doe2", "email": "john.doe222@example.com"})
        print(data)
        id = data["id"]

        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "User updated successfully"
        })
        print(f"Testing PUT /users/{id} with valid update data")
        data, status = put(f"users/{id}", {"first_name": "Jane", "last_name": "Doe"})
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "User updated successfully")

        mock_put.return_value = Mock(status_code=400, json=lambda: {
            "error": "Invalid input data"
        })
        print(f"Testing PUT /users/{id} with invalid input")
        data, status = put(f"users/{id}", {"first_name": "A" * 51})
        print(f"Expected: 400, Actual: {status}, Data: {data}")

        self.assertEqual(status, 400)
        self.assertEqual(data["error"], "Invalid input data")


class TestAmenityEndpoint(unittest.TestCase):

    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    def test_amenity_endpoint(self, mock_put, mock_get, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "name": "WI-FI"
        })
        print("Testing POST /amenities with valid input")
        data, status = post("amenities", {"name": "WI-FI"})
        print(f"Expected: 201, Actual: {status}, Data: {data}")

        self.assertEqual(status, 201)
        self.assertEqual(data["name"], "WI-FI")

        id = data["id"]

        mock_get.return_value = Mock(status_code=200, json=lambda: [
            {"name": "WI-FI"}, {"name": "hello"}
        ])

        post("amenities", {"name": "Fibre"})
        print("Testing GET /amenities")
        data, status = get("amenities")
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "WI-FI")

        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "Amenity successfully created"
        })
        print(f"Testing PUT /amenities/{id} with valid update")
        data, status = put(f"amenities/{id}", {"name": "Wiwi"})
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Amenity successful updated")

class TestPlaceEndpoint(unittest.TestCase):

    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    @patch('requests.delete')
    def test_place_endpoint(self, mock_delete, mock_put, mock_get, mock_post):
        # Test POST /places
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "id": "place-id", "title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0,
            "latitude": 37.7749, "longitude": -122.4194, "owner_id": "user-id", "amenities": []
        })
        print("Testing POST /places with valid input")
        data, status = post("places", {
            "title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0,
            "latitude": 37.7749, "longitude": -122.4194, "owner_id": "user-id", "amenities": []
        })
        print(f"Expected: 201, Actual: {status}, Data: {data}")
        self.assertEqual(status, 201)
        self.assertEqual(data["title"], "Cozy Apartment")
        place_id = data["id"]

        # Test GET /places/{id}
        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "id": place_id, "title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0,
            "latitude": 37.7749, "longitude": -122.4194, "owner_id": "user-id", "amenities": []
        })
        print(f"Testing GET /places/{place_id}")
        data, status = get(f"places/{place_id}")
        print(f"Expected: 200, Actual: {status}, Data: {data}")
        self.assertEqual(status, 200)
        self.assertEqual(data["title"], "Cozy Apartment")

        # Test PUT /places/{id}
        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "Place updated successfully"
        })
        print(f"Testing PUT /places/{place_id} with valid update data")
        data, status = put(f"places/{place_id}", {"title": "Luxury Apartment", "price": 150.0})
        print(f"Expected: 200, Actual: {status}, Data: {data}")
        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Place updated successfully")

        # Test DELETE /places/{id}
        mock_delete.return_value = Mock(status_code=200, json=lambda: {
            "message": "Place deleted successfully"
        })
        print(f"Testing DELETE /places/{place_id}")
        data, status = req(f"places/{place_id}", "DELETE")
        print(f"Expected: 200, Actual: {status}, Data: {data}")
        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Place deleted successfully")

class TestReviewEndpoint(unittest.TestCase):

    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    @patch('requests.delete')
    def test_review_endpoint(self, mock_delete, mock_put, mock_get, mock_post):
        # Test POST /reviews
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "id": "review-id", "text": "Great place!", "rating": 5, "place_id": "place-id", "user_id": "user-id"
        })
        print("Testing POST /reviews with valid input")
        data, status = post("reviews", {
            "text": "Great place!", "rating": 5, "place_id": "place-id", "user_id": "user-id"
        })
        print(f"Expected: 201, Actual: {status}, Data: {data}")
        self.assertEqual(status, 201)
        self.assertEqual(data["text"], "Great place!")
        review_id = data["id"]

        # Test GET /reviews/{id}
        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "id": review_id, "text": "Great place!", "rating": 5, "place_id": "place-id", "user_id": "user-id"
        })
        print(f"Testing GET /reviews/{review_id}")
        data, status = get(f"reviews/{review_id}")
        print(f"Expected: 200, Actual: {status}, Data: {data}")
        self.assertEqual(status, 200)
        self.assertEqual(data["text"], "Great place!")

        # Test PUT /reviews/{id}
        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "Review updated successfully"
        })
        print(f"Testing PUT /reviews/{review_id} with valid update")
        data, status = put(f"reviews/{review_id}", {"text": "Amazing place!", "rating": 4})
        print(f"Expected: 200, Actual: {status}, Data: {data}")
        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Review updated successfully")

        # Test DELETE /reviews/{id}
        mock_delete.return_value = Mock(status_code=200, json=lambda: {
            "message": "Review deleted successfully"
        })
        print(f"Testing DELETE /reviews/{review_id}")
        data, status = req(f"reviews/{review_id}", "DELETE")
        print(f"Expected: 200, Actual: {status}, Data: {data}")
        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Review deleted successfully")


if __name__ == '__main__':
    unittest.main()
