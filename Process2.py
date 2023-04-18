# 用于查询
import Tools
import Socket
import time 
idx = Tools.load_obj('idx3')
mod = Tools.load_obj('mod3')
enc_data_dictionary = Tools.load_obj('encoded data')

nxt_ip = '10.176.34.170'
nxt_port = 8007
pre_ip = '10.176.34.170'
pre_port = 8005
party = 3

s = Socket.Socket(nxt_ip,nxt_port)
s.socket_create()
s.socket_bind()
s.socket_listen(5)
s.socket_reuse()
time.sleep(3)
c = Socket.Socket(pre_ip, pre_port)
c.socket_create()
c.socket_connect()

while True:
    client_socket, client_addr = s.socket_accept()
    while True:
        choose = int(c.socket_recv())
        rnd = int(c.socket_recv())
        data = int(c.socket_recv())
        if(rnd < party):
            data = Tools.get_enc_data(data, idx, mod)
            s.socket_send(client_socket,choose)
            s.socket_send(client_socket,rnd+1)
            s.socket_send(client_socket,data)
        if(rnd >= party and rnd < 2*party):
            if(choose == 1):
                print("此次查询已结束")
                break
            else:
                if(enc_data_dictionary.get(data)):
                    enc_data_dictionary[data]+=1
                else:
                    enc_data_dictionary = 1
                s.socket_send(client_socket,choose)
                s.socket_send(client_socket,rnd+1)
                s.socket_send(client_socket,data)
            