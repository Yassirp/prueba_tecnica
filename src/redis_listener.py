import json
import threading
from socketio_config import socketio
from database.redis import redis_client

def listen_to_redis():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('inventory_alerts')

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            print("📢 Enviando alerta por socket:", data)
            socketio.emit('inventory_alert', data)

def start_redis_listener():
    thread = threading.Thread(target=listen_to_redis)
    thread.daemon = True
    thread.start()
