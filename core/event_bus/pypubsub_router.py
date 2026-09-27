import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventBus")

class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type: str, handler):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(handler)

    def publish(self, event_type: str, data: dict = None):
        logger.info(f"[EVENT BUS] {event_type} | Data: {data}")
        if event_type in self.listeners:
            for handler in self.listeners[event_type]:
                handler(data)

event_bus = EventBus()
