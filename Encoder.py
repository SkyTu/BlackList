import random
import time

class Encoder:
    ciphertext = 1
    
    def __init__(self, index_number, mod_number, plaintext = 1):
        self.index_number = index_number
        self.mod_number = mod_number
        self.plaintext = plaintext
       
    def update_plaintext(self, plaintext):
        self.plaintext = int(plaintext)

    def encode(self):
        index_number = self.index_number
        self.ciphertext = 1#初始化
        if(index_number == 0):
            print("指数为0！")
        while(index_number!=0):
            if(index_number&1):
                self.ciphertext*=self.plaintext
                self.ciphertext%=self.mod_number
            index_number = index_number>>1
            self.ciphertext=(self.ciphertext*self.ciphertext)%self.mod_number