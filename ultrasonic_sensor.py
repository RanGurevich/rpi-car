from gpiozero import DistanceSensor

trigPin = 24
echoPin = 21
sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=3)

def get_distance():
    try:
        distance_cm = sensor.distance * 100
        return distance_cm
    except Exception as e:
        print(f"Error reading ultrasonic sensor: {e}")
        return None

def print_distance():
    distance = get_distance()
    if distance is not None:
        print(f'Distance: {distance:.2f} cm')
    return distance
