#!/usr/bin/python3
"""
Contains the app_views of user
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return {'error': 'Not found'}, 404
    all_reviews = storage.all(Review)
    list_of_reviews = []
    for review in all_reviews.values():
        if review.place_id == place_id:
            list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_one_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        return {'error': 'Not found'}, 404
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_one_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        return {'error': 'Not found'}, 404
    storage.delete(review)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_one_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return {'error': 'Not found'}, 404
    if request.is_json:
        data = request.get_json()
        if "user_id" in data:
            user = storage.get(User, data['user_id'])
            if user is None:
                return {'error': 'Missing user_id'}, 404
            if "text" in data:
                new_dict = dict(data, **{'place_id': place_id})
                new_review = Review(**new_dict)
                storage.new(new_review)
                storage.save()
                return jsonify(new_review.to_dict()), 201
            return {'error': 'Missing text'}, 400
        return {'error': 'Missing user_id'}, 400
    return {'error': 'Not a JSON'}, 400


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_one_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        return {'error': 'Not found'}, 404
    if request.is_json:
        data = request.get_json()
        if "text" in data:
            for key, value in data.items():
                setattr(review, key, value)
            storage.save()
            return jsonify(review.to_dict())
        return {'error': 'Missing text'}, 400
    return {'error': 'Not a JSON'}, 400
