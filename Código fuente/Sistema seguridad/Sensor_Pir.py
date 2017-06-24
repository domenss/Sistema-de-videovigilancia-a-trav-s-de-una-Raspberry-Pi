import RPi.GPIO as GPIO
GPIO_PIR = 21

class Sensor_Pir():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_PIR, GPIO.IN)

    def deteccion(self):
        return GPIO.input(GPIO_PIR)

