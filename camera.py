import cv2
import asyncio
import base64
from picamera2 import Picamera2
from ultralytics import YOLO
from ultraSonic import print_distance
from findObjects import getObjectFound, updateObjectFound

model = YOLO('yolov8n.pt') 

camera = Picamera2()
cameraConfig = camera.create_preview_configuration(main={"size": (1292, 972), "format": "RGB888"})
camera.configure(cameraConfig)
camera.start()


async def startVideoBroadcast(clientConnected):
    print("Starting video broadscast")
    try:
        import time
        timeDelay = time.time()
        
        while True:
            currentTime = time.time()
            if currentTime - timeDelay < 0.05:
                await asyncio.sleep(0.01)
                continue
            timeDelay = currentTime

            frame = camera.capture_array()

            itemsFound = model(frame, stream=True, verbose=False, imgsz=320, conf=0.5)            
            annotated_frame = None
            for itemFound in itemsFound:
                annotated_frame = itemFound.plot()
                updateObjectFound(itemFound)
              

            if annotated_frame is None:
                annotated_frame = frame

            smallFrame = cv2.resize(annotated_frame, (320, 240))
            
            FrameToBroadcast = cv2.cvtColor(smallFrame, cv2.COLOR_RGB2BGR)

            if clientConnected:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
                _, buffer = cv2.imencode('.jpg', FrameToBroadcast, encode_param)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                
                tasks = [client.send(jpg_as_text) for client in clientConnected]
                await asyncio.gather(*tasks, return_exceptions=True)
            # update the car distance in real time
            distance = print_distance()
            if distance < 10:
                print("Too close")
            
            await asyncio.sleep(0.001)

    except Exception as e:
        print(f"Error in broadcast: {e}")
    finally:
        camera.stop()

