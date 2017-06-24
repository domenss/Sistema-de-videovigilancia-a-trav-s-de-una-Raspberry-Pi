from Constantes import *
from time import localtime, strftime
from telegram import ReplyKeyboardMarkup, KeyboardButton
class Bot_Message():

	def __init__(self, bot):
		self.bot = bot

	def photo_message(self):
		self.bot.sendMessage(chat_id=My_ID, text="Enviando captura. Espere...")

	def send_photo(self):
		self.bot.sendPhoto(chat_id = My_ID, photo=open('/home/pi/sistema-videovigilancia/photo.jpg','rb'))

	def activate_system_message(self):
		self.bot.sendMessage(chat_id = My_ID,text="Sistema de seguridad activado")

	def desactivate_system_message(self):
		self.bot.sendMessage(chat_id=My_ID, text="Sistema de seguridad desactivado.")

	def send_url(self, data_server):
		self.bot.sendMessage(chat_id = My_ID,text="Url video streaming: " + "192.168.1.226:5000/" + data_server.url + "\n\nPassword: " + data_server.password)

	def error_peticion_message(self, peticion_solicitada):
		self.bot.sendMessage(chat_id=My_ID, text="No existe el comando: " + peticion_solicitada)

	def send_start_message(self, keyboard):
		self.bot.sendMessage(chat_id=My_ID,text = TEXTO_INTRODUCTORIO, reply_markup = ReplyKeyboardMarkup(keyboard))

	def send_intruso_message(self):
		self.bot.sendMessage(chat_id = chat_id_intruso, text = "No tienes permisos!")

	def send_time(self):
		self.timex = strftime("Presencia detectada a las: %H:%M:%S", localtime())
		self.bot.sendMessage(chat_id = My_ID,text = self.timex)

	def send_video(self):
		self.bot.sendVideo(chat_id = My_ID, video=open('/home/pi/sistema-videovigilancia/video.mp4','rb'))