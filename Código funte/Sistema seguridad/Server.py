import os
class Server():

	def __init__(self, data_server):
		os.system("sudo /usr/bin/python /home/pi/sistema-videovigilancia/flask/app.py " + data_server.url + " " + data_server.password)