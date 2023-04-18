'''
Author: Xinyu Tu
Date: 2022-08-23 16:38:00
LastEditors: Xinyu Tu
LastEditTime: 2022-09-07 15:51:27
'''
import random
import pandas as pd
import Encoder as Enc
import socket
import sys
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def psudorandom_generator_ll(n_bits):
    return random.SystemRandom().getrandbits(n_bits)

def generate_db(items,begin,name):
    # items: 需要生成多少数据
    # begin: 生成数据的开始数值
    # name: 写入到哪个csv中
    db = list()
    for _ in range(items):
        db.append(begin)
        begin+=2
    temp = pd.DataFrame(db)
    temp.to_csv(name+".csv")
    print("数据创建成功")

def get_enc_data_from_csv(csv_name, index_num, mod_num):#从csv文件中获取加密信息
    # csv_name：数据存储文件名
    # n_bits：加密数据
    # mod_num: 取余数据
    csv = pd.read_csv(csv_name+".csv")
    temp = list()
    e = Enc.Encoder(index_num,mod_num)
    for i in csv.values: # 需要判断i的类型
        
        if(str(i[1])[-1]=='X'):
            i[1] = str(i[1])[:-1]
            print(i[1])
        e.update_plaintext(i[1])
        e.encode()
        temp.append(e.ciphertext)
    return temp


def get_enc_data(data, index_num, mod_num):#加密data
    # csv_name：数据存储文件名
    # n_bits：加密数据
    # mod_num: 取余数据
    e = Enc.Encoder(index_num,mod_num)
    data = str(data)
    if(data[-1] == 'X'):
        data = data[:-1]
    e.update_plaintext(data)
    e.encode()
    return e.ciphertext