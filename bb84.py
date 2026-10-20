from qunetsim.components import Host, Network
from qunetsim.objects import Qubit

import random
import time


# ============================================================
# CONFIGURATION
# ============================================================

TARGET_KEY_LENGTH = 256

# Send more than 256 because roughly half of the
# Alice/Bob basis choices will not match.
NUM_QUBITS = 600


# ============================================================
# NETWORK SETUP
# ============================================================

network = Network.get_instance()

alice = Host('Alice')
bob = Host('Bob')

alice.add_connection('Bob')
bob.add_connection('Alice')

network.add_hosts([alice, bob])
network.start()

alice.start()
bob.start()

print("Alice and Bob started successfully.")


# ============================================================
# STORAGE
# ============================================================

alice_bits = []
alice_bases = []

bob_bits = []
bob_bases = []


# ============================================================
# STEP 1 — ALICE GENERATES RANDOM BITS AND BASES
# ============================================================

print("\n[1] Alice generating random bits and bases...")

for i in range(NUM_QUBITS):

    bit = random.randint(0, 1)
    basis = random.randint(0, 1)

    alice_bits.append(bit)
    alice_bases.append(basis)


print("Alice generated", NUM_QUBITS, "random bits.")
print("Alice generated", NUM_QUBITS, "random bases.")


# ============================================================
# STEP 2 — ALICE PREPARES AND SENDS QUBITS
# ============================================================

print("\n[2] Alice preparing and sending qubits...")

for i in range(NUM_QUBITS):

    q = Qubit(alice)

    bit = alice_bits[i]
    basis = alice_bases[i]

    # -----------------------------------------
    # Encode Alice's bit
    # -----------------------------------------

    if bit == 1:
        q.X()

    # -----------------------------------------
    # Encode Alice's basis
    #
    # basis 0 = Z basis
    # basis 1 = X basis
    # -----------------------------------------

    if basis == 1:
        q.H()

    alice.send_qubit('Bob', q)


print("Alice sent", NUM_QUBITS, "qubits.")

# Allow the simulated network to finish deliveries
time.sleep(2)


# ============================================================
# STEP 3 — BOB CHOOSES BASES AND MEASURES
# ============================================================

print("\n[3] Bob measuring received qubits...")

for i in range(NUM_QUBITS):

    basis = random.randint(0, 1)

    bob_bases.append(basis)

    q = bob.get_qubit('Alice', wait=10)

    if q is None:

        print("ERROR: Bob failed to receive qubit", i)

        network.stop()
        exit()

    # If Bob chooses X basis, rotate before measuring.
    if basis == 1:
        q.H()

    result = q.measure()

    bob_bits.append(result)


print("Bob measured", len(bob_bits), "qubits.")


# ============================================================
# STEP 4 — BASIS SIFTING
# ============================================================

print("\n[4] Alice and Bob comparing bases...")

alice_sifted_key = []
bob_sifted_key = []


for i in range(NUM_QUBITS):

    if alice_bases[i] == bob_bases[i]:

        alice_sifted_key.append(alice_bits[i])
        bob_sifted_key.append(bob_bits[i])


print("Matching bases:", len(alice_sifted_key))


# ============================================================
# STEP 5 — CHECK WHETHER WE HAVE ENOUGH KEY MATERIAL
# ============================================================

if len(alice_sifted_key) < TARGET_KEY_LENGTH:

    print("\nNot enough matching bases.")
    print("Run the program again or increase NUM_QUBITS.")

    network.stop()
    exit()


# Take first 256 sifted bits

alice_key = alice_sifted_key[:TARGET_KEY_LENGTH]
bob_key = bob_sifted_key[:TARGET_KEY_LENGTH]


# ============================================================
# STEP 6 — CONVERT KEYS TO STRINGS
# ============================================================

alice_key_binary = ''.join(map(str, alice_key))
bob_key_binary = ''.join(map(str, bob_key))


# ============================================================
# STEP 7 — VERIFY
# ============================================================

print("\n==========================================")
print("              BB84 RESULT")
print("==========================================")

print("\nAlice key length:", len(alice_key))
print("Bob key length:  ", len(bob_key))

print("\nAlice 256-bit key:")

print(alice_key_binary)

print("\nBob 256-bit key:")

print(bob_key_binary)


print("\n------------------------------------------")

if alice_key == bob_key:

    print("SUCCESS: Alice and Bob keys MATCH!")

else:

    print("FAILED: Alice and Bob keys DO NOT MATCH!")

print("------------------------------------------")


network.stop()
# Save the key only if Alice and Bob agree
if alice_key == bob_key:
    from pathlib import Path

    qll_dir = Path("qll")
    qll_dir.mkdir(parents=True, exist_ok=True)

    with open(qll_dir / "raw_key.txt", "w") as f:
        f.write(alice_key_binary)

    print("\nShared key saved to qll/raw_key.txt")
