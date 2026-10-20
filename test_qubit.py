from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import time

network = Network.get_instance()

alice = Host('Alice')
bob = Host('Bob')

alice.add_connection('Bob')
bob.add_connection('Alice')

network.add_hosts([alice, bob])
network.start()

alice.start()
bob.start()

print("Alice and Bob started")

# Alice creates a qubit
q = Qubit(alice)

# Alice prepares |1>
q.X()

print("Alice created qubit |1>")

# Alice sends the qubit to Bob
alice.send_qubit('Bob', q)

# Give the network time to deliver it
time.sleep(1)

# Bob receives the qubit
received = bob.get_qubit('Alice', wait=10)

if received is not None:

    print("Bob successfully received the qubit!")

    result = received.measure()

    print("Bob measured:", result)

else:

    print("Bob did not receive the qubit")

network.stop()
