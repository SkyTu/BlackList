#！/usr/bin/python3
import socket
import argparse                                                     #实现类似于C语言命令行参数的功能
import Tools
import sys

ciphertext = list()

parser = argparse.ArgumentParser(description="c/s")
parser.add_argument('-ip', type=str, default='10.176.34.170')     #默认ip地址
parser.add_argument('-port', type=int, default=8000)                #默认端口号
args=parser.parse_args()
ip=args.ip
port=args.port
idx = Tools.psudorandom_generator_ll(320)

print('you will connect: ip--{}, port--{}'.format(ip,port))

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    c.connect((ip,port))
    print("Successfully connected!")
except socket.error as e:
    print('Failed connecting...')

while True:
    data = Tools.socket_recv(c)
    print(data)
    info = input()    
    Tools.socket_send(c,info)
    data = Tools.socket_recv(c)                                   #接受数据条数和mod值       
    if not data:                                                  #无输入也退出
        break
    print(data)
    temp = ''
    count = 0
    for i in data:
        if(ord('0')<=ord(i)<=ord('9')):
            temp+=i
            count+=1
        else:
            break
    mod = int(data[count+26:])
    count = int(temp)
    print(count)
    dictionary = dict()
    while(count>0):
        data = int(Tools.socket_recv(c))
        data = Tools.get_enc_data(data,idx,mod)
        if(dictionary.get(data)):
            dictionary[data]+=1
        else:
            dictionary[data]=1
        count-=1

    search = int(input("Input the ID number："))
    print(search)
    print("Encoding...")   # 加密信息
    
    search = Tools.get_enc_data(search, idx, mod)   #加密查询数据数值
    Tools.socket_send(c,search)                     #传输加密信息
    
        
    search = int(Tools.socket_recv(c))
    print("Encoded research element recieved!")
    
    
    if(dictionary.get(search)):
        print("Success!")
    else:
        print("Failed!")
c.close()
