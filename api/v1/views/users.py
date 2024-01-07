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


@app_views.route('/users', methods=['GET'])
def get_all_users():
    users = storage.all(User)
    list_of_users = []
    for user in users.values():
        list_of_users.append(user.to_dict())
    return jsonify(list_of_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_one_user():
    if request.is_json:
        data = request.get_json()
        if "email" in data:
            if "password" in data:
                new_user = User(**data)
                storage.new(new_user)
                storage.save()
                return jsonify(new_user.to_dict()), 201
            return jsonify({'error': 'Missing password'}), 400
        return jsonify({'error': 'Missing email'}), 400
    return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user_data(user_id):
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'Not found'}), 404
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'Not a JSON'}), 400
