# core/event_bus.py
import logging

class EventBus:
    def __init__(self):
        self.subscribers = {}
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type, data=None):
        logging.info(f"Event published: {event_type} | Data: {data}")
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

# Global Event Bus instance
bus = EventBus()
