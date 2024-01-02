#!/usr/bin/python3
"""
Contains the app_views of states
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_all_states():
    all_states = storage.all(State)
    # states_list = []
    # for state in all_states.values():
    #     states_list.append(state.to_dict())
    states_list = [state.to_dict() for state in all_states.values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_one_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(state.to_dict())
    # all_states = storage.all(State)
    # for state in all_states:
    #     if state_id == state.id:
    #         states_list = []
    #         states_list.append(state.to_dict())
    #         return states_list
    # return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_an_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    if request.is_json:
        data = request.get_json()
        if "name" in data:
            new_state = State(**data)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        return jsonify({'error': 'Missing name'}), 400
    return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_data(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    return jsonify({'error': 'Not a JSON'}), 400
