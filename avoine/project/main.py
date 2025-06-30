import random

from project.guardian_angel import GuardianAngel
from project.party import Party

# === Simulate Exchange between Alice and Bob ===

ga_alice = GuardianAngel("GA_Alice")
ga_bob = GuardianAngel("GA_Bob")

alice = Party("Alice", ga_alice)
bob = Party("Bob", ga_bob)


# Step 1: Send the item to the Guardian Angel
alice.send_item_to_ga("Secret Item from Alice")
bob.send_item_to_ga("Secret Item from Bob")

# Step 2: Exchange items between parties
alice.send_item_to_party(alice.get_encrypted_item(), bob)
bob.send_item_to_party(bob.get_encrypted_item(), alice)

# Step 3: Syncronization
random_value = random.randint(100, 1000)
alice.set_random_value(random_value)
bob.set_random_value(random_value)

is_alice_turn = True

for i in range(random_value, -1, -1):
    if is_alice_turn:
        alice.decrease_random_value()
        bob.set_random_value(alice.random_value)
        print(f"[{alice.name}] Decreased random value to {alice.random_value}")
    else:
        bob.decrease_random_value()
        alice.set_random_value(bob.random_value)
        print(f"[{bob.name}] Decreased random value to {bob.random_value}")

    is_alice_turn = not is_alice_turn

    if alice.random_value == 0 or bob.random_value == 0:
        print(f"Synchronization successfully completed!")
        break

# Step 4: Finish exchange
alice.complete_exchange()
bob.complete_exchange()
