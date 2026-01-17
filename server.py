import asyncio
import websockets
from camera import broadcast_frames
from carControls import execute_command

from gpiozero import DistanceSensor
from time import sleep

PORT = 80

all_clients = set()

async def unified_handler(websocket):
    print(f"Client connected: {websocket.remote_address}")
    all_clients.add(websocket)
    try:
        async for message in websocket:
            command = message.strip()
            if command:
                print(f"Received car command: {command}")
                await execute_command(command)
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"Error in handler: {e}")
    finally:
        all_clients.remove(websocket)
        print("Client disconnected")

async def main():
    print(f"WebSocket Server starting on port {PORT}")
    
    async with websockets.serve(unified_handler, "0.0.0.0", PORT):
        print(f"WebSocket Server started on port {PORT}")
        print("Clients can receive camera feed and send car control commands")
        await broadcast_frames(all_clients)

    trigPin = 24
    # ultra sonic sensor
    echoPin = 21
    sensor = DistanceSensor(echo=echoPin, trigger=trigPin ,max_distance=3)
    printUltraSonicData()



            # end of ultra sonic sensor

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")


    def printUltraSonicData():
        while True:
            print('Distance: ', sensor.distance * 100,'cm')
            sleep(1)
