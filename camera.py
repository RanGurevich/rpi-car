import cv2
import asyncio
import base64
from picamera2 import Picamera2
from ultralytics import YOLO
from ultraSonic import print_distance

model = YOLO('yolov8n.pt') 

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1292, 972), "format": "RGB888"})
picam2.configure(config)
picam2.start()


async def broadcast_frames(connected_clients):
    print("Starting broadcast loop...")
    try:
        import time
        last_time = time.time()
        
        while True:
            now = time.time()
            if now - last_time < 0.05:
                await asyncio.sleep(0.01)
                continue
            last_time = now

            frame = picam2.capture_array()

            results = model(frame, stream=True, verbose=False, imgsz=320, conf=0.5)
            
            annotated_frame = None
            for r in results:
                annotated_frame = r.plot()

            if annotated_frame is None:
                annotated_frame = frame

            small_frame = cv2.resize(annotated_frame, (320, 240))
            
            display_frame = cv2.cvtColor(small_frame, cv2.COLOR_RGB2BGR)

            if connected_clients:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
                _, buffer = cv2.imencode('.jpg', display_frame, encode_param)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                
                tasks = [client.send(jpg_as_text) for client in connected_clients]
                await asyncio.gather(*tasks, return_exceptions=True)

            distance = print_distance()
            if distance < 10:
                print("Too close")
            
            await asyncio.sleep(0.001)

    except Exception as e:
        print(f"Error in broadcast: {e}")
    finally:
        picam2.stop()
