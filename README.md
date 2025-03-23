# Hazelcast Project Overview

This project demonstrates how to:
- Start a Hazelcast cluster (server nodes) via `hazelcast.yaml`.
- Interact with the cluster from Python clients (`fill_map_route`, `get_value_route`, `increment_no_locks_route`, `increment_pessimistic_route`, `increment_optimistic_route`).
- Perform distributed increments with or without locks.
- Use a bounded queue with one writer and two readers.
- Observe data distribution and resilience when nodes shut down.

Below is the **project structure**:

```
HAZELCAT-2/
├── routes
│   ├── __init__.py
│   ├── fill_map_route.py
│   ├── get_value_route.py
│   ├── increment_no_locks_route.py
│   ├── increment_optimistic_route.py
│   └── increment_pessimistic_route.py
├── venv/
├── app.py
├── hazelcast_client.py
├── hazelcast-client.yaml
├── hazelcast.yaml
├── reader1.py
├── reader2.py
├── writer.py
├── run_all.sh
├── requirements.txt
└── README.md
```

---

## 1. Installing Dependencies

1. Create or activate your Python virtual environment (`venv`).
2. Install required packages:

```
pip install -r requirements.txt
```

---

## 2. Starting Hazelcast Cluster

1. Make sure `hazelcast.yaml` has your desired settings (including any `map` or `queue` config).
2. For each server node you want to run (e.g., three nodes), use:

```
hz start -c hazelcast.yaml
```

3. Verify logs show multiple members (e.g., `Members [3]`).

**Expected result:**  
- Three running Hazelcast nodes on ports `5701`, `5702`, `5703` (unless ports are occupied or auto-increment is disabled).
- Logs indicating that each node joined the cluster.

---

## 3. Running the Flask App

1. Launch the application with:

```
python app.py
```

2. By default, it runs on port 5100 (unless changed).
3. You can then call routes, for example:
   - `GET /fill_map`
   - `GET /get_value?key=123`
   - `POST /increment_no_locks?key=test&count=10000`
   - And so on.

**Expected result:**  
- The map is filled with entries when calling `/fill_map`.
- You can retrieve the current value by calling `/get_value`.
- Different increment endpoints show various final values and timing information.

---

## 4. Testing Distributed Map Operations

### 4.1 Fill the Map
- Command (using Flask route as example):
  ```
  curl http://127.0.0.1:5100/fill_map
  ```
- **Expected result:**  
  A message confirming 1000 entries have been put into the map.

### 4.2 Get a Value
- Command:
  ```
  curl "http://127.0.0.1:5100/get_value?key=123"
  ```
- **Expected result:**  
  JSON with the retrieved value for key `123`.

### 4.3 Increments (No Locks / Pessimistic / Optimistic)
- Command examples:
  ```
  curl -X POST "http://127.0.0.1:5100/increment_no_locks?key=test&count=10000"
  curl -X POST "http://127.0.0.1:5100/increment_pessimistic?key=test&count=10000"
  curl -X POST "http://127.0.0.1:5100/increment_optimistic?key=test&count=10000"
  ```
- **Expected result:**  
  - **No locks**: final value less than `3 × count` if three clients run simultaneously.
  - **Pessimistic** or **Optimistic**: final value equals `3 × count`. Timing varies.

---

## 5. Bounded Queue

### 5.1 Writer and Readers

There are three separate scripts:
- `writer.py` (puts items into a 10-element queue),
- `reader1.py` (pulls items),
- `reader2.py` (pulls items).

#### Example Usage:

1. In one terminal:
   ```
   python reader1.py
   ```
2. In another:
   ```
   python reader2.py
   ```
3. In a third:
   ```
   python writer.py
   ```

**Expected result:**  
- The queue holds up to 10 items at a time.
- If no reader is running, writer blocks when full.
- Each reader consumes distinct messages; they do not see duplicates.
- Writer completes after inserting 100 items.

---

## 6. Shutting Down Nodes

To observe data redistribution and potential data loss:

- **Single node down**:
  ```
  kill -9 <pid_of_one_node>
  ```
  Hazelcast reassigns partitions to remaining nodes.

- **Two nodes down (sequential)**:
  ```
  kill -9 <pid_node_1>
  # Wait for rebalancing
  kill -9 <pid_node_2>
  ```
  Typically no data loss if backup-count=1, because rebalancing completes before the second node leaves.

- **Two nodes down (simultaneous)**:
  ```
  kill -9 <pid_node_1> <pid_node_2>
  ```
  With `backup-count=1`, partial or total data loss can occur. With `backup-count=2`, data remains intact.

**Expected result:**  
- With `backup-count=1`, an immediate double node failure may cause lost partitions.
- With `backup-count=2`, no data is lost even if two nodes fall at once.

---

## 7. `run_all.sh`

You can automate various operations (like parallel increments) by adding lines in `run_all.sh` similar to:

```
python writer.py &
python reader1.py &
python reader2.py &
wait
```

**Expected result:**  
- All processes start in background and run concurrently.

---

## 8. Reference Report

For a full demonstration log and images, see:
[Project Report](https://docs.google.com/document/d/1uQLfg6rL0b6XRd9QdQS-sk4a4PkUrmCMqfwd9QK54a4/edit?usp=sharing)

---
