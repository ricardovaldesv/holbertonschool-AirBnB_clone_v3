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
