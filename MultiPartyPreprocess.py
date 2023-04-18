import Socket
import Tools
import time

length = 320 #默认加密长度

def act_as_server(ip, port, party):
    s = Socket.Socket(ip, port)
    s.socket_create()
    s.socket_reuse()
    s.socket_bind()
    s.socket_listen(party)
    return s

def act_as_client(ip, port):
    s = Socket.Socket(ip, port)
    s.socket_create()
    s.socket_connect()
    return s

# while(True):
#     party = eval(input("Please input the number of all parties:\n"))
#     nxt_ip = input("Please input the ip of next party:\n")
#     nxt_port = eval(input("Please input the port of next party:\n"))
#     pre_ip = input("Please input the ip of previous party:\n")
#     pre_port = eval(input("Please input the port of previous party:\n"))
#     database_name = input("Please input the csv name where database is restored in:\n")
#     t = eval(input("Please input the time(second) to ensure that all server will be activated:\n"))
#     flag = input("Confirm your input and then input r to continue, other character will make you input these parameters again!\n")

#     if(flag=='r'):
#         break

test_number = input("Choose a none-repeated number from 1 to 3\n")
file_name = test_number+'.txt'
with open(file_name,'r')as file_to_read:
    party = int(file_to_read.readline())
    print(party)
    nxt_ip = file_to_read.readline().strip("\n")
    print(nxt_ip)
    nxt_port = int(file_to_read.readline())
    pre_ip = file_to_read.readline().strip("\n")
    pre_port = int(file_to_read.readline())
    database_name = file_to_read.readline().strip("\n")
    t = int(file_to_read.readline())

        
serv = act_as_server(nxt_ip, nxt_port, party)  #作为服务器的socket套接字
time.sleep(t)                           #等待Server开启时间
clnt = act_as_client(pre_ip, pre_port)  #作为客户端的socket套接字
clnt_socket, clnt_addr = serv.socket_accept()

while(True):    #传输mod数值
    select = eval(input("Choose how to get the value of mod number: 1 refers to generate it psudorandomly and 2 refers to recieve a mod number from another party\n"))
    if(select == 1):
        mod = Tools.psudorandom_generator_ll(length)
        serv.socket_send(clnt_socket,mod)
        mod = int(clnt.socket_recv())
        break
    elif(select == 2):
        mod = int(clnt.socket_recv())
        serv.socket_send(clnt_socket,mod)
        break 
    else:
        print("Wrong input, try again!")
print(mod)

enc_round = 1                                       #初始情况下只加密了自己
enc_data_dictionary = dict()                        #完成n轮加密数据的字典信息，其中n==party总数
unfinished_data = list()                            #未完成所有加密的数据的信息

#本地数据加密开始
idx = Tools.psudorandom_generator_ll(length)        #生成随机指数信息
ctxt = Tools.get_enc_data_from_csv(database_name,idx,mod)   #获取本地数据库数据并加密

serv.socket_send(clnt_socket, enc_round)            #表示加密了第一轮，发送当前加密轮次
serv.socket_send(clnt_socket, len(ctxt))
print("send round",enc_round," and length ",len(ctxt))
for txt in ctxt:
    serv.socket_send(clnt_socket, txt)              #传输所有加密的数据
print("Transition of local data has finished!")

#接收来自其他方的数据
rnd = party*2-1
while(rnd>0):
    enc_round = int(clnt.socket_recv())                 #获得加密的轮次
    length_of_enc_data = int(clnt.socket_recv())        #获得本轮加密数据的总数  
    print("enc_round is",enc_round)
    print("length_of_enc is",length_of_enc_data)
    if(enc_round >= party):                             #如果已经全加密完成了
        count = 0                                       #更新至dict中
        while(count < length_of_enc_data):
            temp = int(clnt.socket_recv())
            unfinished_data.append(temp)                #如果还要继续传递下去则append到未完成的数据中去
            if(enc_data_dictionary.get(temp)):
                enc_data_dictionary[temp]+=1
            else:
                enc_data_dictionary[temp]=1
            count+=1
        if(enc_round < party*2-1):                       #如果还能够继续传递
            print("send round",enc_round," and length unfinished_data",len(unfinished_data))
            serv.socket_send(clnt_socket, enc_round+1)
            serv.socket_send(clnt_socket, len(unfinished_data))
            for data in unfinished_data:
                serv.socket_send(clnt_socket, data)      

    else:
        while(length_of_enc_data>0):                    #加密信息
            data = Tools.get_enc_data(int(clnt.socket_recv()),idx,mod)
            unfinished_data.append(data)
            length_of_enc_data -= 1     
        serv.socket_send(clnt_socket, enc_round+1)
        serv.socket_send(clnt_socket, len(unfinished_data))    
        for data in unfinished_data:   
            serv.socket_send(clnt_socket, data)    
        print("send round",enc_round," and length ",len(unfinished_data))
    unfinished_data = list()
    rnd -= 1
Tools.save_obj(enc_data_dictionary, "encoded data")
Tools.save_obj(mod, "mod"+str(test_number))
Tools.save_obj(idx, "idx"+str(test_number))