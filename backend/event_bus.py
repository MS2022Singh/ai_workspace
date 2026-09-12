from pubsub import pub
from typing import Callable, Any, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventBus")

# Standard Event Topics
TOPIC_USER_SPOKE = "system.user_spoke"
TOPIC_INTENT_DETECTED = "system.intent_detected"
TOPIC_TOOL_REQUESTED = "system.tool_requested"
TOPIC_APPROVAL_REQUIRED = "system.approval_required"
TOPIC_TASK_COMPLETED = "system.task_completed"

class EventBusManager:
    def __init__(self):
        self._listeners: Dict[str, list] = {}

    def subscribe(self, topic: str, listener: Callable[..., Any]):
        pub.subscribe(listener, topic)
        if topic not in self._listeners:
            self._listeners[topic] = []
        self._listeners[topic].append(listener)
        logger.info(f"Subscribed {listener.__name__} to topic: {topic}")

    def publish(self, topic: str, **kwargs):
        logger.info(f"Publishing event to '{topic}': {kwargs}")
        pub.sendMessage(topic, **kwargs)

    def unsubscribe(self, topic: str, listener: Callable[..., Any]):
        pub.unsubscribe(listener, topic)
        if topic in self._listeners and listener in self._listeners[topic]:
            self._listeners[topic].remove(listener)
            logger.info(f"Unsubscribed {listener.__name__} from topic: {topic}")

event_bus = EventBusManager()