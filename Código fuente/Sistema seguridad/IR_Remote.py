import lirc
import time
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class IR_Remote():

	def __init__(self, bot_manager):
		sockid = lirc.init("rcled", blocking = False)
		self.logger = logging.getLogger(__name__)
		self.logger.info("__init__IR_Remote")
		self.bot_manager = bot_manager
		self.run()

	def run(self):
		while True:
			try:
				button = lirc.nextcode()
				if len(button) != 0:
					if (button[0]) == 'turn_on_alarm':
						self.logger.info("IR_Remote: encender alarma")
						self.bot_manager.activar_sistema()
					elif (button[0]) == 'turn_off_alarm':
						self.logger.info("IR_Remote: apagar alarma")
						self.bot_manager.desactivar_sistema()
					else:
						pass
				time.sleep(1)
			except KeyboardInterrupt:
				lirc.deinit()
				break




