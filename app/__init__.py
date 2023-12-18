from flask import Flask
from flask_socketio import SocketIO
from .models import Country

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    socketio.init_app(app)

    app.country = Country()

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from .telegram import initialize_telegram_client
    initialize_telegram_client(app, socketio)

    # Import and use socket events
    from . import socket_events  # This import registers the socket event handlers

    return app
