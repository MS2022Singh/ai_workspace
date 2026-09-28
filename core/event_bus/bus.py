import datetime
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self.event_log: List[dict] = []

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: dict = None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "event": event_type, "data": data or {}}
        self.event_log.append(entry)
        
        if event_type in self._subscribers:
            for cb in self._subscribers[event_type]:
                try:
                    cb(entry)
                except Exception as e:
                    print(f"[EVENT BUS ERROR] Handler failure for {event_type}: {e}")
        return entry

event_bus = EventBus()
