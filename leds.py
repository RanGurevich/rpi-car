from gpiozero import LED

GREEN_LED_PIN = 25
RED_LED_PIN = 12
greenLed = LED(GREEN_LED_PIN)
redLed = LED(RED_LED_PIN)

def turnOnGreenLed():
    greenLed.on()

def turnOnRedLed():
    redLed.on()

def turnOffGreenLed():
    greenLed.off()

def turnOffRedLed():
    redLed.off()

def turnOffAllLeds():
    greenLed.off()
    redLed.off()