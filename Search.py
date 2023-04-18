# 用于查询
import Tools
import Socket
import time
idx = Tools.load_obj('idx1')
mod = Tools.load_obj('mod1')
enc_data_dictionary = Tools.load_obj('encoded data')

nxt_ip = '10.176.34.170'    # 本机ip地址
nxt_port = 8005
pre_ip = '10.176.34.170'    # 连接目标服务器的ip地址
pre_port = 8006
party = 3

s = Socket.Socket(nxt_ip,nxt_port)
s.socket_create()
s.socket_bind()
s.socket_listen(5)
s.socket_reuse()
time.sleep(3)               # 等待间隔时间
c = Socket.Socket(pre_ip, pre_port)
c.socket_create()
c.socket_connect()

while True:
    client_socket, client_addr = s.socket_accept()
    while True:
        choose = int(input("输入1表示做查询操作，输入2表示做更新操作，其他输入的数字表示退出"))
        if(choose == 1 or choose == 2):
            s.socket_send(client_socket,choose)#表示做查询/更新操作
            s.socket_send(client_socket,1)#表示已经完成第一轮加密
            data = Tools.get_enc_data(eval(input("输入数据：\n")),idx,mod)
            s.socket_send(client_socket,data)
        else:
            break
        choose = int(c.socket_recv()) #获取选择
        rnd = int(c.socket_recv()) #获取加密轮次
        data = int(c.socket_recv())
        print(data)
        if(choose == 2 and rnd < 2*party):
            s.socket_send(client_socket,choose)
            s.socket_send(client_socket,rnd+1)
            s.socket_send(client_socket,data)
            if(enc_data_dictionary.get(data)):
                enc_data_dictionary[data]+=1
            else:
                enc_data_dictionary[data]=1
            print("数据更新成功")
        else:
            if(enc_data_dictionary.get(data)):
                print("查找成功，此ID共出现了"+str(enc_data_dictionary[data])+"次")
            else:
                print("查找失败")
