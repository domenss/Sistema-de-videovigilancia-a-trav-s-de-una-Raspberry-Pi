#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import logging
from time import localtime, strftime
import os
from Data_Server import URL_Token
My_ID = '117224417'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from Server import Server
class Hilo_Server(threading.Thread):
    
    def __init__(self, data_server):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.logger.info("__init__ HILO_SERVER")
        self.data_server = data_server
        threading.Thread(target = self.run).start()

    def run(self):
        self.logger.info("Ejecutando servidor...")
        Server(self.data_server)
        self.data_server.estado = True
        self.logger.info("Servidor detenido")
                
            
from Sensor_Pir import Sensor_Pir

class Hilo_PIR(threading.Thread):

    def __init__(self, pi_camera, bot_message):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.logger.info("__init__Hilo PIR")
        self.pi_camera = pi_camera
        self.bot_message = bot_message
        self.sensor_pir = Sensor_Pir()
        self.sistema_activo = True
        self.timex = ""
        self.tr = threading.Thread(target = self.run)

    def start(self):
        self.tr.start()

    def stop(self):
        self.sistema_activo = False

    def run(self):
        self.logger.info("Sensor Pir: listo")
        while self.sistema_activo:
            if self.sensor_pir.deteccion():
                self.logger.info("Presencia detectada!")
                self.bot_message.send_time()
                self.pi_camera.capture_photo()
                Hilo_Send_Photo_To_RaspberryWeb()
                self.logger.info("Enviando captura...")
                Hilo_Send_Photo(self.bot_message)
                self.pi_camera.capture_video()
                os.system("MP4Box -add /home/pi/sistema-videovigilancia/video.h264 /home/pi/sistema-videovigilancia/video.mp4")
                Hilo_Send_Video_To_RaspberryWeb()
                Hilo_Buzzer()
                #os.system("rm /home/pi/sistema-videovigilancia/video.mp4")
                self.logger.info("Enviando video...")
                self.bot_message.send_video()
                self.sensor_pir = Sensor_Pir()
                self.logger.info("Video enviado")

class Hilo_Send_Photo(threading.Thread):

    def __init__(self, bot_message):
        threading.Thread.__init__(self)
        self.bot_message = bot_message
        threading.Thread(target = self.run).start()

    def run(self):
        self.bot_message.send_photo()

class Hilo_Send_Photo_To_RaspberryWeb(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread(target = self.run).start()

    def run(self):
        nombre = strftime("%d-%b-%Y_%H-%M-%S", localtime())
        os.system("mv /home/pi/sistema-videovigilancia/photo.jpg " + "/home/pi/sistema-videovigilancia/"+nombre+".jpg")
        os.system("scp /home/pi/sistema-videovigilancia/" + nombre+".jpg " +"pi@192.168.1.225:/home/pi/flask/static/data/")
        os.system("rm /home/pi/sistema-videovigilancia/" + nombre+".jpg")

class Hilo_Send_Video_To_RaspberryWeb(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread(target = self.run).start()

    def run(self):
        nombre = strftime("%d-%b-%Y_%H-%M-%S", localtime())
        os.system("mv /home/pi/sistema-videovigilancia/video.mp4 " + "/home/pi/sistema-videovigilancia/"+nombre+".mp4")
        os.system("scp /home/pi/sistema-videovigilancia/" + nombre+".mp4 " +"pi@192.168.1.225:/home/pi/flask/static/data/")
        os.system("rm /home/pi/sistema-videovigilancia/" + nombre+".mp4")
        
from Buzzer import Buzzer
class Hilo_Buzzer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread(target = self.run).start()
        
    def run(self):
        Buzzer()

from IR_Remote import IR_Remote
class Hilo_IR_Remote(threading.Thread):

    def __init__(self, bot_manager):
        threading.Thread.__init__(self)
        self.bot_manager = bot_manager
        threading.Thread(target = self.run).start()


    def run(self):
        IR_Remote(self.bot_manager)

        
