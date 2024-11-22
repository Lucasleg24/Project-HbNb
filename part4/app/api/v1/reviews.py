from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        user_id = review_data.get("user_id", None)
        place_id = review_data.get("place_id", None)
        current_user = get_jwt_identity()

        #print(current_user)
        #print(review_data["user_id"])

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Invalid place id"}, 404

        if current_user["id"] != user_id:
            return {"error": "Unauthorized action"}, 403

        try:
            new_review = facade.create_review(review_data)
        except Exception as e:
            return {"error": "Invalid input data"}, 400

        place.reviews.append(new_review)
        return {"id": new_review.id, "text": new_review.text, "rating": new_review.rating, "place_id": new_review.place_id, "user_id": new_review.user_id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [{"id": i.id, "text": i.text, "rating": i.rating, "place_id": i.place_id, "user_id": i.user_id} for i in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        obj = facade.get_review(review_id)
        if not obj:
            return {"Error": "Review not found"}, 404
        return {
    "id": obj.id,
    "text": obj.text,
    "rating": obj.rating,
}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        # Get the review to update
        current_user = get_jwt_identity()
        obj = facade.get_review(review_id)
        if not obj:
            return {"error": "Review not found"}, 404

        if not current_user["is_admin"]:
            if current_user["id"] != obj.user_id:
                return {"error": "Unauthorized action"}, 403

        try:
            facade.update_review(review_id, api.payload)
        except Exception as ve:
            return {"error": "Invalid input data"}, 400

        return {"message": "Review updated successfully"}, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review_data = facade.get_review(review_id)

        if not review_data:
            return {"error": 'Review not found'}, 404

        # Si l'utilisateur est un admin, il peut supprimer la critique
        if not current_user["is_admin"]:
            # Si ce n'est pas un admin, il doit être le propriétaire de la critique
            if review_data.user_id != current_user['id']:
                return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)

        return {"message": "Review deleted successfully"}, 200

@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            return {"Error": "place not found"}, 404
        return [{"id": review.id, "text": review.text, "rating": review.rating, "user_id": review.user_id} for review in place.reviews], 200
