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

        print(current_user)
        print(review_data["user_id"])

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
    "place_id": obj.place_id,
    "user_id": obj.user_id
}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        # Get the review to update
        obj = facade.get_review(review_id)
        if not obj:
            return {"Error": "Review not found"}, 404

        current_user = get_jwt_identity()

        # Extract updated data from the request payload
        review_data = api.payload

        if review_data['owner'] != current_user['id']:
            return {'error': 'Unauthorized to update a review'}, 403

        try:
            updated_review = facade.update_review(obj, review_data)  # Pass both obj and review_data
        except Exception as e:
            return {"Error": str(e)}, 400  # Return the error if update fails

        if updated_review is None:
            return {"Error": "Failed to update review"}, 500  # Handle failure in update

        return {
            "id": updated_review.id,
            "text": updated_review.text,
            "rating": updated_review.rating,
            "place_id": updated_review.place_id,
            "user_id": updated_review.user_id
        }, 200



    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""

        current_user = get_jwt_identity()

        review_data = facade.review_repo(review_id)
        print(review_data)

        if review_data['owner'] != current_user['id']:
            return {'error': 'Unauthorized to delete a review'}, 403

        if review_id in self.data:
            del self.data[review_id]
            return {"message": "Review delete successfully"}, 200
        else:
            return {"message": "Review not found"}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {"Error": "place not found"}, 404
        return [{"id": review.id, "text": review.text, "rating": review.rating} for review in reviews], 200
