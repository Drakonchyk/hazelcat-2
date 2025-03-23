import hazelcast

def main():
    client = hazelcast.HazelcastClient(
        cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
    )
    queue = client.get_queue("my-bounded-queue").blocking()

    print("Reader2 started. Will read until queue is empty and writer is done.")

    count = 0
    while True:
        item = queue.poll(timeout=2)
        if item is None:
            print("Reader2: queue empty, finishing reading.")
            break
        count += 1
        print(f"Reader2 got: {item}")

    print(f"Reader2 finished. Total items read: {count}")
    client.shutdown()

if __name__ == "__main__":
    main()
