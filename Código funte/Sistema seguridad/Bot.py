#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Constantes import *
from Bot_Manager import Bot_Manager
import logging
from Hilo import Hilo_IR_Remote
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class Raspi_Bot():

    def __init__(self, Camara_Pi):
        self.logger = logging.getLogger(__name__)
        self.logger.info("__init__")
        self.pi_camera = Camara_Pi
        self.main()

    def start(self, bot, update):
        if self.isValid_chat_id(update.message.chat_id):
            self.logger.info("start")
            self.bot_manager = Bot_Manager(bot, update, self.pi_camera)
            self.bot_manager.configurar_keyboard()
            Hilo_IR_Remote(self.bot_manager)
        else:
            self.bot_manager.mensaje_intruso(update.message.chat_id)

    def executar_peticion(self, bot, update):
        self.logger.info("executar_peticion: " + update.message.text)
        
        if self.isValid_chat_id(update.message.chat_id):
             peticion_solicitada = update.message.text

             if peticion_solicitada == 'Captura instantanea':
                 self.bot_manager.captura_instantanea()

             elif peticion_solicitada == 'Activar sistema':
                 self.bot_manager.activar_sistema()
	
    	     elif peticion_solicitada == 'Desactivar Sistema':
                 self.bot_manager.desactivar_sistema()
    	
    	     elif peticion_solicitada == "Video Streaming":
                 self.bot_manager.video_streaming()
    	
    	     else:
                 self.bot_manager.error(peticion_solicitada)
                
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text = "No tienes permisos!")

    def main(self):
        updater = Updater(TOKEN)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(MessageHandler(Filters.text,self.executar_peticion))	

        updater.start_polling()
        updater.idle()

    def isValid_chat_id(self, chat_id):
        if (str(chat_id) == My_ID):
            return True
        else:
            return False

