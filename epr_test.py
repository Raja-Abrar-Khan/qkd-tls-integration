from qunetsim.components import Host, Network

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

alice.send_epr('Bob')

epr = bob.get_epr('Alice', wait=10)

if epr is not None:
    print("EPR pair successfully created!")
    result = epr.measure()
    print("Bob measured:", result)
else:
    print("Failed to receive EPR pair")

network.stop()
