from pubsub import pub

def publish_event(event_type, data):
    pub.sendMessage(event_type, data=data)

def subscribe_event(event_type, handler):
    pub.subscribe(handler, event_type)
