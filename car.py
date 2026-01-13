from gpiozero import Robot
from time import sleep

# הגדרת הפינים - שנה את המספרים אם חיברת לפינים אחרים ב-Pi
# left=(IN1_PIN, IN2_PIN), right=(IN3_PIN, IN4_PIN)
robby = Robot(left=(17, 27), right=(22, 23))

print("Control the car with the keyboard:")
print("w: Forward")
print("s: Backward")
print("a: Left (Spin)")
print("d: Right (Spin)")
print("q: Stop")
print("e: Exit program")

# הגדרת מהירות (בין 0 ל-1)
speed = 1

try:
    while True:
        # שימוש ב-input (מתאים לפייתון 3)
        command = input("Enter command: ").lower()

        if command == 'w':
            print("Going Forward")
            robby.forward(speed)
        
        elif command == 's':
            print("Going Backward")
            robby.backward(speed)
        
        elif command == 'a':
            print("Turning Left")
            # סיבוב במקום: גלגל אחד קדימה, שני אחורה
            robby.left(speed)
        
        elif command == 'd':
            print("Turning Right")
            robby.right(speed)
        
        elif command == 'q':
            print("Stopping")
            robby.stop()

        elif command == 'e':
            print("Exiting...")
            robby.stop()
            break
            
        else:
            print("Unknown command, try w, s, a, d, q")

except KeyboardInterrupt:
    print("\nProgram stopped by user")
    robby.stop()