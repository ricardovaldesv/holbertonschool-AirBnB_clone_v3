#!/usr/bin/python3
"""
Contains the app_views of places
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_all_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return {'error': 'Not found'}, 404
    all_places = storage.all(Place)
    list_of_places = []
    for place in all_places.values():
        if place.city_id == city_id:
            list_of_places.append(place.to_dict())
    return jsonify(list_of_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_one_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return {'error': 'Not found'}, 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_one_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return {'error': 'Not found'}, 404
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_new_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return {'error': 'Not found'}, 404
    if request.is_json:
        data = request.get_json()
        if "user_id" in data:
            user = storage.get(User, data['user_id'])
            if user is None:
                return jsonify({'error': 'Not found'}), 404
            if "name" in data:
                new_data = dict(data, **{'city_id': city_id})
                new_place = Place(**new_data)
                storage.new(new_place)
                storage.save()
                return jsonify(new_place.to_dict()), 201
            return jsonify({'error': 'Missing name'}), 400
        return jsonify({'error': 'Missing user_id'}), 400
    return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place_data(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return {'error': 'Not found'}, 404
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    return jsonify({'error': 'Not a JSON'}), 400
