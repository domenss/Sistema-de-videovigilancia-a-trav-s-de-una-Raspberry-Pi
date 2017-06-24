from Constantes import *
from telegram import ReplyKeyboardMarkup, KeyboardButton
from Data_Server import URL_Token
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from Hilo import Hilo_Server, Hilo_PIR, Hilo_IR_Remote
from Constantes import *
from Bot_Message import Bot_Message

class Bot_Manager():

    def __init__(self, bot, update, pi_camera):
        self.logger = logging.getLogger(__name__)
        self.logger.info("__init__")
        self.bot_message = Bot_Message(bot)
        self.pi_camera = pi_camera
        self.update = update
        self.data_server = URL_Token()


    def captura_instantanea(self):
        self.logger.info("Comando: Captura instantanea")
        self.pi_camera.capture_photo()
        self.logger.info("Enviando captura...")
        self.bot_message.photo_message()
        self.bot_message.send_photo()
        self.logger.info("Captura enviada")

    def activar_sistema(self):
    	self.logger.info("Comando: Activar Sistema")
    	self.bot_message.activate_system_message()
    	self.hilo_pir = Hilo_PIR(self.pi_camera, self.bot_message)
    	self.hilo_pir.start()

    def desactivar_sistema(self):
    	try:
            self.hilo_pir.stop()
            self.logger.info("Comando: Desactivar Sistema")
            self.bot_message.desactivate_system_message()
        except:
            self.bot_message.desactivate_system_message()
        self.logger.info("Sistema desactivado")

    def video_streaming(self):
        self.logger.info("Comando: Video Streaming")
        if self.data_server.estado == True:
            self.data_server = URL_Token()
            self.data_server.estado = False
            self.bot_message.send_url(self.data_server)
            Hilo_Server(self.data_server)
            self.logger.info("enviando datos server")
        else:
            self.bot_message.send_url(self.data_server)

    def error(self, peticion_solicitada):
    	peticion_solicitada = update.message.text
    	self.bot_message.error_peticion_message(peticion_solicitada)
    	self.logger.error("Se ha introducido un comando erroneo")

    def configurar_keyboard(self):
    	keyboard = [[KeyboardButton("Activar sistema")], [KeyboardButton("Desactivar Sistema")], [KeyboardButton("Captura instantanea")],[KeyboardButton("Video Streaming")]]
    	self.bot_message.send_start_message(keyboard)

    def mensaje_intruso(self, chat_id_intruso):
    	self.bot_message.send_intruso_message(chat_id_intruso)