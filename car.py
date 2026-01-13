from gpiozero import Motor
from time import sleep

# --- הגדרת 4 המנועים לפי החיבורים שלך ---

# צד שמאל (Left)
# קדמי: 17, 27 | אחורי: 5, 6
# תיקון כיוון: החלפת forward/backward בגלל בעיית חומרה
front_left = Motor(forward=27, backward=17)
rear_left = Motor(forward=6, backward=5)

# צד ימין (Right)
# קדמי: 22, 23 | אחורי: 13, 19
# תיקון כיוון: החלפת forward/backward בגלל בעיית חומרה
front_right = Motor(forward=23, backward=22)
rear_right = Motor(forward=19, backward=13)

print("Control the 4WD car with the keyboard:")
print("w: Forward (כל הגלגלים קדימה)")
print("s: Backward (כל הגלגלים אחורה)")
print("a: Left (סיבוב במקום שמאלה)")
print("d: Right (סיבוב במקום ימינה)")
print("q: Stop (עצירה)")
print("e: Exit program")

# הגדרת מהירות (בין 0 ל-1)
speed = 0.3

def stop_all():
    front_left.stop()
    rear_left.stop()
    front_right.stop()
    rear_right.stop()

try:
    while True:
        # קבלת פקודה מהמשתמש
        command = input("Enter command: ").lower()

        if command == 'w':
            print("Going Forward")
            # הפעלת צד שמאל וצד ימין קדימה
            front_left.backward(speed)
            rear_left.forward(speed)
            front_right.backward(speed)
            rear_right.forward(speed)
        
        elif command == 's':
            print("Going Backward")
            # הפעלת צד שמאל וצד ימין אחורה
            front_left.backward(speed)
            rear_left.backward(speed)
            front_right.backward(speed)
            rear_right.backward(speed)
        
        elif command == 'a':
            print("Turning Left")
            # סיבוב טנק: שמאל אחורה, ימין קדימה
            front_left.backward(speed)
            rear_left.backward(speed)
            front_right.forward(speed)
            rear_right.forward(speed)
        
        elif command == 'd':
            print("Turning Right")
            # סיבוב טנק: שמאל קדימה, ימין אחורה
            front_left.forward(speed)
            rear_left.forward(speed)
            front_right.backward(speed)
            rear_right.backward(speed)
        
        elif command == 'q':
            print("Stopping")
            stop_all()

        elif command == 'e':
            print("Exiting...")
            stop_all()
            break
            
        else:
            print("Unknown command, try w, s, a, d, q")

except KeyboardInterrupt:
    print("\nProgram stopped by user")
    stop_all()