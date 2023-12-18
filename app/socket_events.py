from flask import request, current_app
from . import socketio

authenticated_clients = set()

@socketio.on('connect')
def connect():
    auth_key = request.args.get('auth_key')
    if auth_key in current_app.config['AUTH_KEYS']:
        authenticated_clients.add(request.sid)
    else:
        return False  # Reject the connection if auth_key is not valid

@socketio.on('disconnect')
def disconnect():
    authenticated_clients.discard(request.sid)

def send_event(event_data):
    for client_sid in authenticated_clients:
        socketio.emit('event', event_data, room=client_sid)
