import socket
import sys 

class Socket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    def update_ip(self, ip):
        self.ip = ip

    def update_port(self, ip):
        self.ip = ip
    
    def socket_create(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created...')
    

    def socket_reuse(self):
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        print('Sever ip can be reused in a short time now!')

    def socket_bind(self):
        try:
            self.s.bind((self.ip, self.port))
        except socket.error as e:
            print('Failed binding...',e)
            sys.exit(0)
    
    def socket_accept(self):
        return self.s.accept()

    def socket_listen(self, time):
        self.s.listen(5)
    
    def socket_connect(self):
        try:
            self.s.connect((self.ip,self.port))
            print("Successfully connected!")
        except socket.error as e:
            print('Failed connecting...')


    def socket_recv(self):
        # socket_s: 套接字
        data = bytes()
        n_byte = self.s.recv(4).decode('utf-8','ignore')
        # while(n_byte==''):
        #     n_byte = self.s.recv(4).decode('utf-8','ignore')
        n_byte = int(n_byte)
        while True:
            data += self.s.recv(n_byte - len(data))
            if(len(data)==n_byte):
                break
        return data.decode('utf-8','ignore')


    def socket_send(self, socket_s, info):
        # socket_s: 套接字
        # info: 需要传输的字符
        length = str(len(str(info))).zfill(4)
        info = length+str(info)
        socket_s.send(info.encode('utf-8'))
