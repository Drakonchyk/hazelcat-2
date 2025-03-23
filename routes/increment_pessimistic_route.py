from flask import Blueprint, request, jsonify
from hazelcast_client import distributed_map
import time
import threading

increment_pessimistic_blueprint = Blueprint("increment_pessimistic_blueprint", __name__)

def increment_pessimistic_fn(key, count):
    for _ in range(count):
        distributed_map.lock(key)
        try:
            val = distributed_map.get(key)
            val += 1
            distributed_map.put(key, val)
        finally:
            distributed_map.unlock(key)

@increment_pessimistic_blueprint.route("/increment_pessimistic", methods=["POST"])
def increment_pessimistic():
    key = request.args.get("key", "demo")
    count = int(request.args.get("count", 10000))

    distributed_map.put(key, 0)

    t1 = threading.Thread(target=increment_pessimistic_fn, args=(key, count))
    t2 = threading.Thread(target=increment_pessimistic_fn, args=(key, count))
    t3 = threading.Thread(target=increment_pessimistic_fn, args=(key, count))

    start_time = time.time()

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

    end_time = time.time()

    final_value = distributed_map.get(key)
    duration = end_time - start_time

    return jsonify({
        "message": (
            f"3 threads with PESSIMISTIC lock, each did {count} increments on key='{key}'."
        ),
        "final_value": final_value,
        "expected_value": 3 * count,
        "time_seconds": duration
    })
