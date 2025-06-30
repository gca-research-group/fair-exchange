import threading
import time
from datetime import datetime, timedelta


class GuardianAngel:
    def __init__(self, name, timeout_seconds=5):
        self.name = name
        self.sessions = {}
        self.timeout_seconds = timeout_seconds

    def set_item(self, session_id, item):
        self.sessions[session_id]["item"] = item

    def set_party_item(self, party_name, item):
        if party_name not in self.sessions:
            print(
                f"[{self.name}] WARNING: No active session for {party_name}. Starting a new session."
            )
            self.start_session(party_name)
        print(f"[{self.name}] Setting item for {party_name}: {item}")
        self.sessions[party_name]["party_item"] = item

    def start_session(self, party_name):
        session_id = f"{party_name}_{int(time.time())}"
        self.sessions[session_id] = {
            "last_seen": datetime.now(),
            "active": True,
            "party": party_name,
            "item": None,
            "party_item": False,
        }
        print(f"[{self.name}] Session started for {party_name} with ID {session_id}")
        threading.Thread(target=self._watchdog, args=(session_id,), daemon=True).start()
        return session_id

    def keep_in_touch(self, session_id):
        if session_id in self.sessions and self.sessions[session_id]["active"]:
            self.sessions[session_id]["last_seen"] = datetime.now()
            # print(f"[{self.name}] KiT from {session_id} at {self.sessions[session_id]['last_seen']}")
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
                print(
                    f"[{self.name}] TIMEOUT: {session_id} is unresponsive. Triggering recovery."
                )
                self.sessions[session_id]["active"] = False
            time.sleep(1)
