from flask import Flask, render_template, request
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
    global document_state
    emit('update_document', document_state)
    print("New connection event\n")
    emit('request_name')


@socketio.on('register_name')
def handle_register_name(data):
    global clients
    client_id = request.sid     # unique session id of the client
    name = data['name']
    clients[client_id] = name
    print(f"Client connected: {data['name']}\n")
    update_client_list()


def update_client_list():
    global clients
    client_names = list(clients.values())
    emit('update_client_list', client_names, broadcast=True)


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
    global clients
    client_id = request.sid
    if client_id in clients:
        print(f"Client disconnected: {clients[client_id]}\n")
        del clients[client_id]
    update_client_list()
    # emit('update_cursors', cursor_positions, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, "localhost", 3000, debug=True) 