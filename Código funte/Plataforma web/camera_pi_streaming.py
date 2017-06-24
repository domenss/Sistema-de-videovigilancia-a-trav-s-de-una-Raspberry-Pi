import time
import os
import io
import threading
import picamera
import socket
import struct
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        
        server_socket = socket.socket()
        server_socket.bind(('', 8000))
        time.sleep(1)
        Hilo_Pi_Bot()
        server_socket.listen(0)
        connection = server_socket.accept()[0].makefile('rb')

        
        while True:
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))

            # store frame
            image_stream.seek(0)
            cls.frame = image_stream.read()

            # reset stream for next frame
            image_stream.seek(0)
            image_stream.truncate()


class Hilo_Pi_Bot(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread(target = self.run).start()


    def run(self):
        os.system("ssh pi@192.168.1.226 python piBot.py") 