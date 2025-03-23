from flask import Blueprint, request, jsonify
from hazelcast_client import distributed_map
import time
import threading

increment_no_locks_blueprint = Blueprint("increment_no_locks_blueprint", __name__)

def increment_no_locks_fn(key, count):
    """
    Функція, яку виконуватиме кожен потік (псевдо-клієнт):
    - count разів виконує:
        val = map.get(key)
        val++
        map.put(key, val)
    """
    for _ in range(count):
        val = distributed_map.get(key)
        val += 1
        distributed_map.put(key, val)

@increment_no_locks_blueprint.route("/increment_no_locks", methods=["POST"])
def increment_no_locks():
    key = request.args.get("key", "demo")
    count = int(request.args.get("count", 10000))

    distributed_map.put(key, 0)

    t1 = threading.Thread(target=increment_no_locks_fn, args=(key, count))
    t2 = threading.Thread(target=increment_no_locks_fn, args=(key, count))
    t3 = threading.Thread(target=increment_no_locks_fn, args=(key, count))

    start_time = time.time()

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    end_time = time.time()

    final_value = distributed_map.get(key)
    elapsed = end_time - start_time

    return jsonify({
        "message": (
            f"3 threads (no locks) incremented key={key}, each did {count} increments. "
            f"Ideally {3*count}, got {final_value} (race conditions expected)."
        ),
        "final_value": final_value,
        "expected_value": 3 * count,
        "time_seconds": elapsed
    })
