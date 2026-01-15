from gpiozero import Motor
from time import sleep

# --- הגדרת המנועים ---
frontRightWheel = Motor(forward=27, backward=17)
backLeftWheel = Motor(forward=6, backward=5)
frontLeftWheel = Motor(forward=23, backward=22)
backRightWheel = Motor(forward=19, backward=13)

# הגדרות מהירות
MIN_MOMENTOM_FOR_SPEED = 0.5
normalSpeed = 0.7
speed = normalSpeed 
speedForTurning = 1 
speedForStrafing = 1 

# --- כיול הזמן לסיבוב ---
# שנה את המספר הזה עד שהרובוט יסתובב בדיוק 45 מעלות
# מספר גדול יותר = סיבוב גדול יותר
TURN_TIME_22_DEG = 0.2 

# --- פונקציות עוטפות (התיקון שלך נשמר) ---
def frontRightWheelBackward():
    frontRightWheel.backward(speed)

def frontRightWheelForward():
    frontRightWheel.forward(speed)

def frontLeftWheelForward():
    frontLeftWheel.backward(speed) # תיקון הלחמה

def frontLeftWheelBackward():
    frontLeftWheel.forward(speed) # תיקון הלחמה

def backLeftWheelFoward():
    backLeftWheel.backward(speed) # תיקון הלחמה

def backLeftWheelBackward():
    backLeftWheel.forward(speed) # תיקון הלחמה

def backRightWheelFoward():
    backRightWheel.forward(speed)    

def backRightWheelBackward():
    backRightWheel.backward(speed)    

def stop_all():
    frontRightWheel.stop()
    backLeftWheel.stop()
    frontLeftWheel.stop()
    backRightWheel.stop()

# --- תפריט ---
print("--- Mecanum Control (Discrete Turning) ---")
print("w: Forward | s: Backward")
print("a: Turn Left 45° | d: Turn Right 45°")
print("z: Strafe Left | c: Strafe Right")
print("u/i/j/k: Diagonals")
print("q: Stop | e: Exit")

try:
    while True:
        command = input("Enter command: ").lower()

        # === נסיעה רגילה ===
        if command == 'w':
            speed = normalSpeed
            print("Going Forward")
            frontRightWheelForward()
            frontLeftWheelForward()
            backLeftWheelFoward()
            backRightWheelFoward()
        
        elif command == 's':
            speed = normalSpeed
            print("Going Backward")
            frontRightWheelBackward()
            frontLeftWheelBackward()
            backLeftWheelBackward()
            backRightWheelBackward()

        # === סיבוב במקום 45 מעלות ===
        # כאן השינוי הגדול: אנחנו מפעילים, מחכים ועוצרים
        elif command == 'a':
            print(f"Turning Left 45 degrees ({TURN_TIME_22_DEG}s)...")
            speed = speedForTurning
            
            # התחלת סיבוב
            frontRightWheelForward()
            backRightWheelFoward()
            frontLeftWheelBackward()
            backLeftWheelBackward()
            
            # המתנה לזמן המוגדר
            sleep(TURN_TIME_22_DEG)
            
            # עצירה אוטומטית
            stop_all()
        
        elif command == 'd':
            print(f"Turning Right 45 degrees ({TURN_TIME_22_DEG}s)...")
            speed = speedForTurning
            
            # התחלת סיבוב
            frontLeftWheelForward()
            backLeftWheelFoward()
            frontRightWheelBackward()
            backRightWheelBackward()
            
            # המתנה לזמן המוגדר
            sleep(TURN_TIME_22_DEG)
            
            # עצירה אוטומטית
            stop_all()

        # === גלישה הצידה (Strafing) ===
        elif command == 'z':
            print("Strafe Left")
            speed = speedForStrafing
            frontLeftWheelBackward()
            frontRightWheelForward()
            backLeftWheelFoward()
            backRightWheelBackward()

        elif command == 'c':
            print("Strafe Right")
            speed = speedForStrafing
            frontLeftWheelForward()
            frontRightWheelBackward()
            backLeftWheelBackward()
            backRightWheelFoward()

        # === אלכסונים ===
        elif command == 'u':
            print("Diagonal: Forward-Left")
            speed = normalSpeed
            frontRightWheelForward()
            backLeftWheelFoward()
            frontLeftWheel.stop()
            backRightWheel.stop()

        elif command == 'i':
            print("Diagonal: Forward-Right")
            speed = normalSpeed
            frontLeftWheelForward()
            backRightWheelFoward()
            frontRightWheel.stop()
            backLeftWheel.stop()

        elif command == 'j':
            print("Diagonal: Backward-Left")
            speed = normalSpeed
            frontLeftWheelBackward()
            backRightWheelBackward()
            frontRightWheel.stop()
            backLeftWheel.stop()

        elif command == 'k':
            print("Diagonal: Backward-Right")
            speed = normalSpeed
            frontRightWheelBackward()
            backLeftWheelBackward()
            frontLeftWheel.stop()
            backRightWheel.stop()

        # === יציאה ===
        elif command == 'q':
            print("Stopping")
            stop_all()

        elif command == 'e':
            print("Exiting...")
            stop_all()
            break
            
        else:
            print("Unknown command.")

except KeyboardInterrupt:
    print("\nProgram stopped by user")
    stop_all()