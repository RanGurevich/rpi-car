from gpiozero import Motor
from time import sleep
from ultraSonic import getDistance
import asyncio
from findObjects import getFoundObjects, updateObjectFound

frontRightWheel = Motor(forward=27, backward=17)
backLeftWheel = Motor(forward=6, backward=5)
frontLeftWheel = Motor(forward=23, backward=22)
backRightWheel = Motor(forward=19, backward=13)

MIN_MOMENTOM_FOR_SPEED = 0.5
normalSpeed = 0.5
speedForTurning = 0.8
speedForStrafing = 0.3

mission_finished = False 

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

async def stopCarFunc():
    await frontRightWheel.stop()
    await backLeftWheel.stop()
    await frontLeftWheel.stop()
    await backRightWheel.stop()

async def driveForward(timeToDrive):
    if mission_finished:
        return
    speed = normalSpeed
    frontRightWheelForward(speed)
    frontLeftWheelForward(speed)
    backLeftWheelFoward(speed)
    backRightWheelFoward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCarFunc()

async def driveBackward(timeToDrive):
    if mission_finished:
        return
    speed = normalSpeed
    frontRightWheelBackward(speed)
    frontLeftWheelBackward(speed)
    backLeftWheelBackward(speed)
    backRightWheelBackward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCarFunc()

async def turnLeft(timeToDrive):
    if mission_finished:
        return
    speed = speedForTurning
    frontRightWheelForward(speed)
    backRightWheelFoward(speed)
    frontLeftWheelBackward(speed)
    backLeftWheelBackward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCarFunc()

async def turnRight(timeToDrive):
    if mission_finished:
        return
    speed = speedForTurning
    frontLeftWheelForward(speed)
    backLeftWheelFoward(speed)
    frontRightWheelBackward(speed)
    backRightWheelBackward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCarFunc()

async def searchItem(itemName):
    global mission_finished
    
    if mission_finished:
        return

    while True:
        if mission_finished:
            break

        oldDistance = getDistance()
        await asyncio.sleep(0.1)
        
        if(getDistance() > 20):
            await driveForward(0.5)
            newDistance = getDistance()
            if(int(newDistance) == int(oldDistance)):
                await driveBackward(0.8)
                await turnLeft(0.4)
        else:
            await turnLeft(0.6)
            await driveBackward(0.5)

        itemFound = getFoundObjects()
        print(f"Found objects: {itemFound}")
        
        if itemName in itemFound:
            print(f"Found {itemName}")
            mission_finished = True 
            await stopCarFunc()
            return

async def runDriveCommand(command):
    global mission_finished
    
    if mission_finished:
        return

    command = command.lower().strip()
    
    if command == 'reset_mission':
        mission_finished = False
        return

    if command == 'forward':
        await driveForward(0.5)
        
    elif command == 'backward':
        await searchItem('banana')

    elif command == 'left':
        await turnLeft(0.3)
        
    elif command == 'right':
        await turnRight(0.3)

    elif command == 'z':
        print("Strafe Left")
        speed = speedForStrafing
        frontLeftWheelBackward(speed)
        frontRightWheelForward(speed)
        backLeftWheelFoward(speed)
        backRightWheelBackward(speed)
        await asyncio.sleep(1.0)
        await stopCarFunc()

    elif command == 'c':
        print("Strafe Right")
        speed = speedForStrafing
        frontLeftWheelForward(speed)
        frontRightWheelBackward(speed)
        backLeftWheelBackward(speed)
        backRightWheelFoward(speed)
        await asyncio.sleep(1.0)
        await stopCarFunc()

    elif command == 'u':
        print("Diagonal: Forward-Left")
        speed = normalSpeed
        frontRightWheelForward(speed)
        backLeftWheelFoward(speed)
        frontLeftWheel.stop()
        backRightWheel.stop()
        await asyncio.sleep(1.0)
        await stopCarFunc()

    elif command == 'i':
        print("Diagonal: Forward-Right")
        speed = normalSpeed
        frontLeftWheelForward(speed)
        backRightWheelFoward(speed)
        frontRightWheel.stop()
        backLeftWheel.stop()
        await asyncio.sleep(1.0)
        await stopCarFunc()

    elif command == 'j':    
        print("Diagonal: Backward-Left")
        speed = normalSpeed
        frontLeftWheelBackward(speed)
        backRightWheelBackward(speed)
        frontRightWheel.stop()
        backLeftWheel.stop()
        await asyncio.sleep(1.0)
        await stopCarFunc()

    elif command == 'k':    
        print("Diagonal: Backward-Right")
        speed = normalSpeed
        frontRightWheelBackward(speed)
        backLeftWheelBackward(speed)
        frontLeftWheel.stop()
        backRightWheel.stop()
        await asyncio.sleep(1.0)
        await stopCarFunc()

    elif command == 'stop':
        await stopCarFunc()

    else:
        await searchItem(command)