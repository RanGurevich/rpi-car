from gpiozero import Motor
from time import sleep
from ultraSonic import getDistance
import asyncio
from findObjects import getFoundObjects, updateObjectFound
from leds import turnOnGreenLed, turnOnRedLed, turnOffGreenLed, turnOffRedLed, turnOffAllLeds

frontRightWheel = Motor(forward=27, backward=17)
backLeftWheel = Motor(forward=6, backward=5)
frontLeftWheel = Motor(forward=23, backward=22)
backRightWheel = Motor(forward=19, backward=13)

MIN_MOMENTOM_FOR_SPEED = 0.5
normalSpeed = 0.5
speedForTurning = 0.8
speedForStrafing = 0.3



TURN_TIME_22_DEG = 0.5 
FORWARD_BACKWARD_TIME = 0.2
TIME_FOR_USER_DRIVE = 0.5

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

async def stopCar():
    frontRightWheel.stop()
    backLeftWheel.stop()
    frontLeftWheel.stop()
    backRightWheel.stop()

async def driveForward(timeToDrive):
    speed = normalSpeed
    frontRightWheelForward(speed)
    frontLeftWheelForward(speed)
    backLeftWheelFoward(speed)
    backRightWheelFoward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCar()

async def driveBackward(timeToDrive):
    speed = normalSpeed
    frontRightWheelBackward(speed)
    frontLeftWheelBackward(speed)
    backLeftWheelBackward(speed)
    backRightWheelBackward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCar()

async def turnLeft(timeToDrive):
    speed = speedForTurning
    frontRightWheelForward(speed)
    backRightWheelFoward(speed)
    frontLeftWheelBackward(speed)
    backLeftWheelBackward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCar()

async def turnRight(timeToDrive):
    speed = speedForTurning
    frontLeftWheelForward(speed)
    backLeftWheelFoward(speed)
    frontRightWheelBackward(speed)
    backRightWheelBackward(speed)
    await asyncio.sleep(timeToDrive)
    await stopCar()

async def searchItem(itemName):
    turnOffAllLeds()
    while True:
        turnOnRedLed()
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
        print(f"!!!!!!!!!!!!!!!Found objects: {itemFound}")
        if(itemName in itemFound):
            turnOffRedLed()
            turnOnGreenLed()
            await stopCar()
            # item found but not entering to the condition
            print(f"Found {itemName} and stopping car")
            await asyncio.sleep(15)
            turnOffAllLeds()
            await stopCar()
            break
        

async def runDriveCommand(command):
    # ניקוי מקיף של הפקודה - הסרת כל תווים לא-מודפסים
    original_command = command
    command = ''.join(char for char in command if char.isprintable())
    command = command.lower().strip()
    
    print(f"DEBUG: Original command: {repr(original_command)}, Cleaned: '{command}' (len={len(command)})")
    
    if command == 'forward':
        await driveForward(0.5)
        return
        
    elif command == 'backward':
        await driveBackward(0.5)
        return
        #await searchItem('banana')
        #turnOnRedLed()
        #turnOnGreenLed()

    elif command == 'left':
        await turnLeft(0.3)
        return
        
    elif command == 'right':
        await turnRight(0.3)
        return

    elif command == 'z':
        print("Strafe Left")
        speed = speedForStrafing
        frontLeftWheelBackward(speed)
        frontRightWheelForward(speed)
        backLeftWheelFoward(speed)
        backRightWheelBackward(speed)
        await asyncio.sleep(1.0)
        await stopCar()
        return

    elif command == 'c':
        print("Strafe Right")
        speed = speedForStrafing
        frontLeftWheelForward(speed)
        frontRightWheelBackward(speed)
        backLeftWheelBackward(speed)
        backRightWheelFoward(speed)
        await asyncio.sleep(1.0)
        await stopCar()
        return

    elif command == 'u':
        print("Diagonal: Forward-Left")
        speed = normalSpeed
        frontRightWheelForward(speed)
        backLeftWheelFoward(speed)
        frontLeftWheel.stop()
        backRightWheel.stop()
        await asyncio.sleep(1.0)
        await stopCar()
        return

    elif command == 'i':
        print("Diagonal: Forward-Right")
        speed = normalSpeed
        frontLeftWheelForward(speed)
        backRightWheelFoward(speed)
        frontRightWheel.stop()
        backLeftWheel.stop()
        await asyncio.sleep(1.0)
        await stopCar()
        return

    elif command == 'j':
        print("Diagonal: Backward-Left")
        speed = normalSpeed
        frontLeftWheelBackward(speed)
        backRightWheelBackward(speed)
        frontRightWheel.stop()
        backLeftWheel.stop()
        await asyncio.sleep(1.0)
        await stopCar()
        return

    elif command == 'k':
        print("Diagonal: Backward-Right")
        speed = normalSpeed
        frontRightWheelBackward(speed)
        backLeftWheelBackward(speed)
        frontLeftWheel.stop()
        backRightWheel.stop()
        await asyncio.sleep(1.0)
        await stopCar()
        return

    elif command == 'stop':
        await stopCar()
        return

    else:
        await searchItem(command)

