import asyncio
import websockets
from camera import broadcast_frames
from carControls import execute_command

CAMERA_PORT = 80
CAR_CONTROL_PORT = 8080

camera_clients = set()
car_control_clients = set()

async def camera_handler(websocket):
    print(f"Camera client connected: {websocket.remote_address}")
    camera_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        camera_clients.remove(websocket)
        print("Camera client disconnected")

async def car_control_handler(websocket):
    print(f"Car control client connected: {websocket.remote_address}")
    car_control_clients.add(websocket)
    try:
        async for message in websocket:
            command = message.strip()
            print(f"Received car command: {command}")
            await execute_command(command)
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"Error in car control handler: {e}")
    finally:
        car_control_clients.remove(websocket)
        print("Car control client disconnected")

async def main():
    print(f"Camera WebSocket Server starting on port {CAMERA_PORT}")
    print(f"Car Control WebSocket Server starting on port {CAR_CONTROL_PORT}")
    
    async with websockets.serve(camera_handler, "0.0.0.0", CAMERA_PORT), \
             websockets.serve(car_control_handler, "0.0.0.0", CAR_CONTROL_PORT):
        print(f"Camera WebSocket Server started on port {CAMERA_PORT}")
        print(f"Car Control WebSocket Server started on port {CAR_CONTROL_PORT}")
        await broadcast_frames(camera_clients)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
