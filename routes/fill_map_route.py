from flask import Blueprint
from hazelcast_client import distributed_map

fill_map_blueprint = Blueprint("fill_map_blueprint", __name__)

@fill_map_blueprint.route("/fill_map", methods=["GET"])
def fill_map():
    """
    Заповнює мапу 1000 значеннями: ключі 0..999
    """
    data = {i: f"value-{i}" for i in range(1000)} 
    distributed_map.put_all(data)
    return "Map has been filled with 1000 entries (keys 0..999).", 200
