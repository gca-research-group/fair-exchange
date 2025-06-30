import time
import threading
from datetime import datetime, timedelta

class GuardianAngel:
    def __init__(self, name, timeout_seconds=5):
        self.name = name
        self.sessions = {}
        self.timeout_seconds = timeout_seconds

    def start_session(self, party_name):
        session_id = f"{party_name}_{int(time.time())}"
        self.sessions[session_id] = {
            "last_seen": datetime.now(),
            "active": True,
            "party": party_name
        }
        print(f"[{self.name}] Session started for {party_name} with ID {session_id}")
        threading.Thread(target=self._watchdog, args=(session_id,), daemon=True).start()
        return session_id

    def keep_in_touch(self, session_id):
        if session_id in self.sessions and self.sessions[session_id]["active"]:
            self.sessions[session_id]["last_seen"] = datetime.now()
            print(f"[{self.name}] KiT from {session_id} at {self.sessions[session_id]['last_seen']}")
        else:
            print(f"[{self.name}] WARNING: Session {session_id} is inactive or unknown")

    def end_session(self, session_id):
        if session_id in self.sessions:
            self.sessions[session_id]["active"] = False
            print(f"[{self.name}] Session {session_id} ended normally.")

    def _watchdog(self, session_id):
        while self.sessions[session_id]["active"]:
            last_seen = self.sessions[session_id]["last_seen"]
            if datetime.now() - last_seen > timedelta(seconds=self.timeout_seconds):
                print(f"[{self.name}] TIMEOUT: {session_id} is unresponsive. Triggering recovery.")
                self.sessions[session_id]["active"] = False
            time.sleep(1)

class Party:
    def __init__(self, name, guardian_angel):
        self.name = name
        self.ga = guardian_angel
        self.session_id = self.ga.start_session(name)

    def do_step(self, description, delay=2):
        print(f"[{self.name}] Step: {description}")
        self.ga.keep_in_touch(self.session_id)
        time.sleep(delay)

    def complete_exchange(self):
        self.ga.end_session(self.session_id)
        print(f"[{self.name}] Exchange completed.")

# === Simulate Exchange between Alice and Bob ===

ga_alice = GuardianAngel("GA_Alice")
ga_bob = GuardianAngel("GA_Bob")

alice = Party("Alice", ga_alice)
bob = Party("Bob", ga_bob)

# Step 1: Alice sends encrypted item
alice.do_step("Send encrypted item to Bob")

# Step 2: Bob receives and sends receipt
bob.do_step("Receive item and send receipt")



# Step 3: Alice receives receipt and sends key
alice.do_step("Receive receipt and send decryption key")

# Step 4: Bob decrypts the item
# bob.do_step("Decrypt item")
time.sleep(2)

# Step 5: Finish exchange
alice.complete_exchange()
bob.complete_exchange()
