import cv2
import asyncio
import websockets
import base64
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO

PORT = 80

model = YOLO('yolov8n.pt') 

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1292, 972), "format": "RGB888"})
picam2.configure(config)
picam2.start()

connected_clients = set()

async def handler(websocket):
    print(f"Client connected: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")

async def broadcast_frames():
    print("Starting broadcast loop...")
    try:
        # משתנה עזר לחישוב זמנים
        import time
        last_time = time.time()
        
        while True:
            # 1. מניעת הצפה: אם עבר מעט מדי זמן, נחכה קצת כדי לא לחנוק את המעבד
            # זה נשמע מוזר, אבל זה נותן למעבד זמן לטפל בתקשורת רשת
            now = time.time()
            if now - last_time < 0.05: # מגביל למקסימום 20 פריימים בשנייה
                await asyncio.sleep(0.01)
                continue
            last_time = now

            # לכידת פריים
            frame = picam2.capture_array()

            # 2. טריק לביצועים: במקום לרוץ על כל התמונה, YOLO ירוץ על תמונה קטנה
            # אבל נצייר את התוצאות על התמונה המקורית
            results = model(frame, stream=True, verbose=False, imgsz=320, conf=0.5)
            
            annotated_frame = None
            for r in results:
                annotated_frame = r.plot() # הציור לוקח זמן מעבד!

            if annotated_frame is None:
                annotated_frame = frame

            # 3. ה-Game Changer: הקטנת התמונה לשידור
            # המרה ל-JPG של תמונה 640x480 לוקחת המון מעבד.
            # נוריד אותה ל-320x240 רק לצורך השידור (YOLO עדיין ראה הכל)
            # זה מוריד 75% מהעומס על ה-imencode!
            small_frame = cv2.resize(annotated_frame, (320, 240))
            
            # המרה לצבעים (הלקוח מצפה ל-BGR כי הוא דפדפן, אבל OpenCV זה BGR... רגע)
            # Picamera נותן RGB, OpenCV רוצה BGR
            display_frame = cv2.cvtColor(small_frame, cv2.COLOR_RGB2BGR)

            if connected_clients:
                # דחיסה אגרסיבית יותר
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
                _, buffer = cv2.imencode('.jpg', display_frame, encode_param)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                
                # שליחה "בלי לחכות יותר מדי"
                # אם יש המון לקוחות זה יכול לעכב, אבל עם אחד זה בסדר
                tasks = [client.send(jpg_as_text) for client in connected_clients]
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # שחרור קריטי למערכת ההפעלה
            await asyncio.sleep(0.001)

    except Exception as e:
        print(f"Error in broadcast: {e}")
    finally:
        picam2.stop()
        
async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"WebSocket Server started on port {PORT}")
        await broadcast_frames()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")