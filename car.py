from gpiozero import Motor
from time import sleep




frontRightWheel = Motor(forward=27, backward=17)
backLeftWheel = Motor(forward=6, backward=5)


frontLeftWheel = Motor(forward=23, backward=22)
backRightWheel = Motor(forward=19, backward=13)

def frontRightWheelBackward():
    frontRightWheel.backward(speed)

def frontRightWheelForward():
    frontRightWheel.forward(speed)

def frontLeftWheelForward():
    frontLeftWheel.backward(speed)

def frontLeftWheelBackward():
    frontLeftWheel.forward(speed)

def backLeftWheelFoward():
    backLeftWheel.backward(speed)    

def backLeftWheelBackward():
    backLeftWheel.forward(speed)

def backRightWheelFoward():
    backRightWheel.forward(speed)   

def backRightWheelBackward():
    backRightWheel.backward(speed)   

    



print("w: Forward")
print("s: Backward ")
print("a: Left ")
print("d: Right ")
print("q: Stop ")
print("e: Exit program")


MIN_MOMENTOM_FOR_SPEED = 0.5
normalSpeed = 1 # MIN_MOMENTOM_FOR_SPEED + 0.3 
speed = normalSpeed 
speedForTurning = 1 #MIN_MOMENTOM_FOR_SPEED + 0.5

def stop_all():
    frontRightWheel.stop()
    backLeftWheel.stop()
    frontLeftWheel.stop()
    backRightWheel.stop()

try:
    while True:

        command = input("Enter command: ").lower()

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


        
        elif command == 'a':
            print("Turning Left")
            speed = speedForTurning
            frontRightWheelForward()
            backRightWheelFoward()
            frontLeftWheelBackward()
            backLeftWheelBackward()
        
        elif command == 'd':
            print("Turning Right")
            speed = speedForTurning
            frontLeftWheelForward()
            backLeftWheelFoward()
            frontRightWheelBackward()
            backRightWheelBackward()

            
        
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