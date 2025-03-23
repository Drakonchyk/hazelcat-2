from flask import Blueprint, request, jsonify
from hazelcast_client import distributed_map

get_value_blueprint = Blueprint("get_value_blueprint", __name__)

@get_value_blueprint.route("/get_value", methods=["GET"])
def get_value():
    key_str = request.args.get("key", None)
    if key_str is None:
        return "No key provided", 400

    try:
        key_int = int(key_str)
    except ValueError:
        return "Key must be an integer if we stored them as int", 400

    val = distributed_map.get(key_int)
    return jsonify({"key": key_int, "value": val})
