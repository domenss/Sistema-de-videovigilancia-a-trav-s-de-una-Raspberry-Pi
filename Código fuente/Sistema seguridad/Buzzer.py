import RPi.GPIO as GPIO
import logging
import time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
MAX_ITERACIONES = 30
PIN_BUZZER = 10
class Buzzer():

	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.logger.info("__init__ Buzzer")
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(10, GPIO.OUT)
		self.execute()

	def execute(self):
		iteracion = 0
		self.logger.info("BUZZER activo")
		while iteracion != MAX_ITERACIONES:
			GPIO.output(PIN_BUZZER, False)
			time.sleep(.1)
			GPIO.output(PIN_BUZZER, True)
			time.sleep(.1)
			iteracion = iteracion + 1
		GPIO.cleanup()
