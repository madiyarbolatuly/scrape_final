# app.py
from api.application import create_app, socketio

# Create the app using the factory
app = create_app()

if __name__ == "__main__":
    # For development with Flask-SocketIO:
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
