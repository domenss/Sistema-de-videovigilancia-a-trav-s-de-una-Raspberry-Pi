from picamera import PiCamera
import os
class Cam_Pi():
    def start_camera(self):
        self.camera = PiCamera()
        self.camera.resolution = (640,480)
        self.camera.start_preview()	

    def capture_photo(self):
        self.start_camera()
        self.camera.capture('/home/pi/sistema-videovigilancia/photo.jpg')
        self.camera.stop_preview()
        self.stop_camera()

    def stop_camera(self):
    	self.camera.stop_preview()
        self.camera.close()

    def capture_video(self):
        self.start_camera()
        self.camera.start_recording('/home/pi/sistema-videovigilancia/video.h264')
        self.camera.wait_recording(5)
        self.camera.stop_recording()
        self.stop_camera()                
