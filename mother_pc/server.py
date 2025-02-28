from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import asyncio
import websockets

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# List of connected child PCs
connected_clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("A client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("A client disconnected")

@socketio.on('send_command')
def handle_command(data):
    """Send command to the selected child PC"""
    pc_name = data.get("pc")
    command = data.get("command")
    
    if pc_name in connected_clients:
        ip = connected_clients[pc_name]
        asyncio.run(send_command_to_child(ip, command))
    else:
        emit("response", {"message": f"PC {pc_name} not connected"})

async def send_command_to_child(ip, command):
    """Send WebSocket message to the child PC"""
    try:
        async with websockets.connect(f"ws://{ip}:8765") as ws:
            await ws.send(json.dumps({"command": command}))
            response = await ws.recv()
            socketio.emit("response", {"message": f"Response from {ip}: {response}"})
    except Exception as e:
        socketio.emit("response", {"message": f"Error connecting to {ip}: {str(e)}"})

@socketio.on('register_child')
def register_child(data):
    """Register child PCs when they connect"""
    pc_name = data.get("pc_name")
    ip = data.get("ip")
    connected_clients[pc_name] = ip
    emit("update_clients", {"clients": list(connected_clients.keys())}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=False)
