from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_random_key'
socketio = SocketIO(app)

document_state = ""
clients = {}

@app.route('/')
def index():
    return render_template('index.html')

# connect, disconnect, and error are reserved keywords for socketio
@socketio.on('connect')
def handle_connect():
    emit('update_document', document_state)
    print("New connection event\n")

@socketio.on('edit')
def handle_edit(data):
    # declare global to specify that we are referring to the already initialized doc_state
    global document_state
    document_state = data['content']
    # broadcast=True: sends event to all connected clients except the one that triggered it.
    # without it, only the user that triggered the edit event would get an update
    emit('update_document', document_state, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconencted\n")

if __name__ == "__main__":
    socketio.run(app, "localhost", 3000, debug=True)