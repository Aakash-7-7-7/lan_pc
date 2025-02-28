import asyncio
import websockets
import json
import os
import socket
import shutil

MOTHER_PC_IP = "__your__ip"  # Change this to your Mother PC's IP
MOTHER_PC_PORT = 3000
FOLDER_PATH = "C:/Users/Admin/Desktop"  # Update with your actual username

async def handle_commands(websocket):
    async for message in websocket:
        data = json.loads(message)
        command = data.get("command")

        if command == "delete":
            file_path = os.path.join(FOLDER_PATH, data.get("file_name", ""))
            if os.path.exists(file_path):
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Delete folder
                    else:
                        os.remove(file_path)  # Delete file
                    response = f"Deleted {file_path}"
                except Exception as e:
                    response = f"Error: {str(e)}"
            else:
                response = "File not found"

        elif command == "list":
            try:
                files = os.listdir(FOLDER_PATH)
                response = f"Files in tt: {', '.join(files)}"
            except Exception as e:
                response = f"Error: {str(e)}"

        else:
            response = "Unknown command"

        await websocket.send(response)

async def start_server():
    async with websockets.serve(handle_commands, "0.0.0.0", 8765):
        print("Child PC WebSocket server running...")
        await asyncio.Future()  # Keep the server running

async def register_with_mother():
    """Register this child PC with the Mother PC"""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    async with websockets.connect(f"ws://{MOTHER_PC_IP}:{MOTHER_PC_PORT}") as ws:
        await ws.send(json.dumps({"event": "register_child", "pc_name": hostname, "ip": ip_address}))

# Run both tasks concurrently
async def main():
    await register_with_mother()
    await start_server()

if __name__ == "__main__":
    asyncio.run(main())
