from gpiozero import DistanceSensor
import time
trigPin = 24
echoPin = 21
sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=3)

carDistance = 0

def getDistance():
    try:
        distanceInCM = sensor.distance * 100
        return distanceInCM
    except Exception as e:
        print(f"Error reading ultrasonic sensor: {e}")
        return None

def print_distance():
    time.sleep(0.1)
    distance = getDistance()
    if distance is not None:
        print(f'Distance: {distance:.2f} cm')
    return distance
