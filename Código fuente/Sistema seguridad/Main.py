
"""Clase principal para poner en marcha el bot"""
from Camara_Pi import Cam_Pi
from Bot import Raspi_Bot
import wiringpi

if __name__ == '__main__':
    Raspi_Bot(Cam_Pi())
