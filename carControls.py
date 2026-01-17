from gpiozero import Motor
from time import sleep
from ultraSonic import getDistance
import asyncio

frontRightWheel = Motor(forward=27, backward=17)
backLeftWheel = Motor(forward=6, backward=5)
frontLeftWheel = Motor(forward=23, backward=22)
backRightWheel = Motor(forward=19, backward=13)

MIN_MOMENTOM_FOR_SPEED = 0.5
normalSpeed = 0.7
speedForTurning = 1
speedForStrafing = 0.3

TURN_TIME_22_DEG = 0.5 
FORWARD_BACKWARD_TIME = 0.2

def frontRightWheelBackward(speed_val):
    frontRightWheel.backward(speed_val)

def frontRightWheelForward(speed_val):
    frontRightWheel.forward(speed_val)

def frontLeftWheelForward(speed_val):
    frontLeftWheel.backward(speed_val)

def frontLeftWheelBackward(speed_val):
    frontLeftWheel.forward(speed_val)

def backLeftWheelFoward(speed_val):
    backLeftWheel.backward(speed_val)

def backLeftWheelBackward(speed_val):
    backLeftWheel.forward(speed_val)

def backRightWheelFoward(speed_val):
    backRightWheel.forward(speed_val)    

def backRightWheelBackward(speed_val):
    backRightWheel.backward(speed_val)    

async def stop_all():
    frontRightWheel.stop()
    backLeftWheel.stop()
    frontLeftWheel.stop()
    backRightWheel.stop()

async def driveForward():
    speed = normalSpeed
    frontRightWheelForward(speed)
    frontLeftWheelForward(speed)
    backLeftWheelFoward(speed)
    backRightWheelFoward(speed)
    await asyncio.sleep(FORWARD_BACKWARD_TIME)
    await stop_all()

async def driveBackward():
    speed = normalSpeed
    frontRightWheelBackward(speed)
    frontLeftWheelBackward(speed)
    backLeftWheelBackward(speed)
    backRightWheelBackward(speed)
    await asyncio.sleep(FORWARD_BACKWARD_TIME)
    await stop_all()

async def turnLeft():
    speed = speedForTurning
    frontRightWheelForward(speed)
    backRightWheelFoward(speed)
    frontLeftWheelBackward(speed)
    backLeftWheelBackward(speed)
    await asyncio.sleep(TURN_TIME_22_DEG)
    await stop_all()

async def turnRight():
    speed = speedForTurning
    frontLeftWheelForward(speed)
    backLeftWheelFoward(speed)
    frontRightWheelBackward(speed)
    backRightWheelBackward(speed)
    await asyncio.sleep(TURN_TIME_22_DEG)
    await stop_all()

async def driveAlone():
    while True:
        if(getDistance() > 20):
            await driveForward()
        else:
            await turnLeft()
            await turnLeft()
            await driveBackward()



async def execute_command(command):
    command = command.lower().strip()
    
    if command == 'forward':
        await driveForward()
        
    elif command == 'backward':
        #await driveBackward()
        await driveAlone()

    elif command == 'left':
        await turnLeft()
        
    elif command == 'right':
        await turnRight()

    elif command == 'z':
        print("Strafe Left")
        speed = speedForStrafing
        frontLeftWheelBackward(speed)
        frontRightWheelForward(speed)
        backLeftWheelFoward(speed)
        backRightWheelBackward(speed)
        await asyncio.sleep(1.0)
        await stop_all()

    elif command == 'c':
        print("Strafe Right")
        speed = speedForStrafing
        frontLeftWheelForward(speed)
        frontRightWheelBackward(speed)
        backLeftWheelBackward(speed)
        backRightWheelFoward(speed)
        await asyncio.sleep(1.0)
        await stop_all()

    elif command == 'u':
        print("Diagonal: Forward-Left")
        speed = normalSpeed
        frontRightWheelForward(speed)
        backLeftWheelFoward(speed)
        frontLeftWheel.stop()
        backRightWheel.stop()
        await asyncio.sleep(1.0)
        await stop_all()

    elif command == 'i':
        print("Diagonal: Forward-Right")
        speed = normalSpeed
        frontLeftWheelForward(speed)
        backRightWheelFoward(speed)
        frontRightWheel.stop()
        backLeftWheel.stop()
        await asyncio.sleep(1.0)
        await stop_all()

    elif command == 'j':
        print("Diagonal: Backward-Left")
        speed = normalSpeed
        frontLeftWheelBackward(speed)
        backRightWheelBackward(speed)
        frontRightWheel.stop()
        backLeftWheel.stop()
        await asyncio.sleep(1.0)
        await stop_all()

    elif command == 'k':
        print("Diagonal: Backward-Right")
        speed = normalSpeed
        frontRightWheelBackward(speed)
        backLeftWheelBackward(speed)
        frontLeftWheel.stop()
        backRightWheel.stop()
        await asyncio.sleep(1.0)
        await stop_all()

    elif command == 'stop':
        await stop_all()


    else:
        print(f"Unknown command: {command}")
