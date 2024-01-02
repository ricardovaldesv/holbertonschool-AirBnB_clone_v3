from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, State, City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in req_json:
        abort(400, 'Missing name')

    req_json['state_id'] = state_id
    new_city = City(**req_json)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')

    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()

    return jsonify(city.to_dict()), 200
