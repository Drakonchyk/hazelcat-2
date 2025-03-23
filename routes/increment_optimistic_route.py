from flask import Blueprint, request, jsonify
from hazelcast_client import distributed_map
import time
import threading

increment_optimistic_blueprint = Blueprint("increment_optimistic_blueprint", __name__)

def increment_optimistic_fn(key, count):
    for _ in range(count):
        while True:
            old_val = distributed_map.get(key)
            new_val = old_val + 1
            replaced = distributed_map.replace_if_same(key, old_val, new_val)
            if replaced:
                break

@increment_optimistic_blueprint.route("/increment_optimistic", methods=["POST"])
def increment_optimistic():
    key = request.args.get("key", "demo")
    count = int(request.args.get("count", 10000))

    distributed_map.put(key, 0)

    t1 = threading.Thread(target=increment_optimistic_fn, args=(key, count))
    t2 = threading.Thread(target=increment_optimistic_fn, args=(key, count))
    t3 = threading.Thread(target=increment_optimistic_fn, args=(key, count))

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
            f"3 threads with OPTIMISTIC lock (CAS), each did {count} increments on key='{key}'."
        ),
        "final_value": final_value,
        "expected_value": 3 * count,
        "time_seconds": duration
    })
