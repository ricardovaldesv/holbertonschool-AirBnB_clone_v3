#!/usr/bin/python3
"""
Contains the app_views of amenities
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    all_amenities = storage.all(Amenity)
    list_of_amenities = []
    for amenity in all_amenities.values():
        list_of_amenities.append(amenity.to_dict())
    return jsonify(list_of_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_one_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_one_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_one_amenity():
    if request.is_json:
        data = request.get_json()
        if "name" in data:
            new_amenity = Amenity(**data)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        return jsonify({'error': 'Missing name'}), 400
    return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity_data(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'error': 'Not found'}), 404
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    return jsonify({'error': 'Not a JSON'}), 400
