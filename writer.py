import hazelcast
import time

def main():
    client = hazelcast.HazelcastClient(
        cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
    )
    queue = client.get_queue("my-bounded-queue").blocking()

    print("Writer started. Will put numbers 1..100 into the queue.")

    for i in range(1, 101):
        queue.put(i)
        print(f"Writer put: {i}")

    print("Writer finished. All 100 elements placed into queue.")
    client.shutdown()

if __name__ == "__main__":
    main()
