
from random import choice
class URL_Token():

    def __init__(self):
        self.url = ""
        self.password = ""
        self.generate_password()
        self.generate_url()
        self.estado = True
    
    def generate_password(self):
        for count in range(4):
            self.password += "%s" % choice("123456789")

    def generate_url(self):
        for count in range(20):
            self.url += "%s" % choice("123456789qwertyuiopasdfghjklzxcvbnm")
