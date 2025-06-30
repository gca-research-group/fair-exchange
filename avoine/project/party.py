import time


class Party:
    def __init__(self, name, guardian_angel):
        self.name = name
        self.ga = guardian_angel
        self.session_id = self.ga.start_session(name)
        self.random_value = 0

    def send_item_to_ga(self, item):
        print(f"[{self.name}] Sending item to Guardian Angel: {item}")
        self.ga.keep_in_touch(self.session_id)
        self.ga.set_item(self.session_id, item)

    def get_encrypted_item(self):
        if self.session_id in self.ga.sessions:
            item = self.ga.sessions[self.session_id].get("item", None)
            if item:
                return item
            else:
                print(f"[{self.name}] No item found in session {self.session_id}.")
        else:
            print(f"[{self.name}] WARNING: Session {self.session_id} not found.")
        return None

    def receive_item(self, item):
        print(f"[{self.name}] Received item: {item}")
        self.ga.keep_in_touch(self.session_id)

    def send_item_to_party(self, item, recipient):
        print(f"[{self.name}] Sending item to {recipient.name}: {item}")
        recipient.receive_item(item)

    def set_random_value(self, value):
        self.random_value = value

    def decrease_random_value(self):
        if self.random_value > 0:
            self.random_value -= 1
        else:
            print(f"[{self.name}] Random value is already zero.")
        self.ga.keep_in_touch(self.session_id)
        time.sleep(0.1)

    def do_step(self, description, delay=2):
        print(f"[{self.name}] Step: {description}")
        self.ga.keep_in_touch(self.session_id)
        time.sleep(delay)

    def complete_exchange(self):
        self.ga.end_session(self.session_id)
        print(f"[{self.name}] Exchange completed.")
