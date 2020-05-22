# coding=utf-8
# 发送方发送消息+关键字信息

import os
import time
import datetime
import sys
import base64

# 将加密后的信息+关键字写入txt文件
def write_in_txt(msg,cypher):
    path = '/home/savoki/test_origin'  # 设置文件夹路径
    str1 = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # 获取当前时间并转化成字符串,作为文件名
    filename=path+"/"+str1+'.txt'
    fp = open(filename, 'a')  # 如果有这个文件就打开，如果没有这个文件就创建一个文件
    string = str(base64.encodestring(msg).decode('utf-8')) # 把字节型转为字符串
    string = string.replace("\r", ""); # 集中成一行，便于之后按行读取
    string = string.replace("\n", "");
    # print(string)
    fp.write(string)
    # print(base64.decodestring(string.encode('utf-8')))
    fp.write("\n")
    [A, B] = cypher
    a=str(A).strip()
    fp.write(a)
    fp.write("\n")
    b=str(B).strip()
    fp.write(b)
    fp.write("\n")
    fp.close()