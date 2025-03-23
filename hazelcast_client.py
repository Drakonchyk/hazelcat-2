import hazelcast

hz_client = hazelcast.HazelcastClient(
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ],
)

distributed_map = hz_client.get_map("my-distributed-map").blocking()
