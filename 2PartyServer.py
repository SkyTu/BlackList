#!/usr/bin/python3
import socket
import sys
import pandas as pd
import Tools
import Encoder as Enc



ip = '10.176.34.170'                                              #默认IP
port = 8000                                                         #默认端口
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
print('Socket created...')

try:
    s.bind((ip,port))
except socket.error as e:
    print('Failed binding...',e)
    sys.exit(0)

s.listen(5)
print("server is running...")
print("Encoding the data...")

idx = Tools.psudorandom_generator_ll(320)
mod = Tools.psudorandom_generator_ll(320)
ciphertext = Tools.get_enc_data_from_csv("data.csv",idx,mod)
# ciphertext = pd.read_csv("data.csv").values.T[1].T
print("The index is："+str(idx)+"\nand mod is："+str(mod))
print("Successfully encoded！")


while True:
    client_socket, client_addr = s.accept()
    while True:
        info = "Connection established, if you need to search the database, please send Yes!"
        Tools.socket_send(client_socket, info)
        data = Tools.socket_recv(client_socket)
        if data=='q':
            break
        print('Confirmation from client is：{}'.format(data))

        info = input('Please select the operations: 1 refers to transit the database and 2 refers to add new data\n')
        if(int(info) == 1):
            info = str(len(ciphertext))+" data and mod number m is:"+str(mod)
            print(info)
            Tools.socket_send(client_socket,info)
            count = 0
            for ctxt in ciphertext:
                Tools.socket_send(client_socket,ctxt)
                count+=1
        elif(info == 2):#更新数据库
            pass
        else:
            pass
        

        search = int(Tools.socket_recv(client_socket))  #获取查询数据
        print("Received the quirey!")

        search = Tools.get_enc_data(search,idx,mod)     #加密search
        print("Encoding the query!")
        
        print("Transiting the encoded query...")
        Tools.socket_send(client_socket, search)
        print(search)
        print("Finished!")
client_socket.close()
