#!/usr/bin/python3
"""
Contains the app_views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def test_status():
    '''Test the status of the route'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def clases_count():
    '''endpoint that retrieves the number of each objects by type'''
    new_dict = {}
    new_dict["amenities"] = storage.count("Amenity")
    new_dict["cities"] = storage.count("City")
    new_dict["places"] = storage.count("Place")
    new_dict["reviews"] = storage.count("Review")
    new_dict["states"] = storage.count("State")
    new_dict["users"] = storage.count("User")
    return jsonify(new_dict)
