# coding=utf-8
# 接受者进行文件检索

import os
from mysite.search_kw.py_files import peks
from pypbc import *

def sh(params, pk, td):
    path = r'/home/savoki/test_origin'  # 设置文件夹路径
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    pairing = Pairing(params)
    ss = []
    for file in files:  # 遍历文件夹
        s=[]
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            f = open(path + "/" + file);  # 打开文件
            iter_f = iter(f);  # 创建迭代器
            print(file)
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                str1 = ""
                str1 = str1 + line
                s.append(str1)  # 每行文本存到list中
                print(str1)
            f.close()
        # print(s[2])
        A=Element(pairing, G1, value=s[1].strip())

        '''
        #按逗号拆分s[2]:格式为：(xxx, xxxx)
        content=s[2]
        i=1 # 去掉括号
        
        while i < len(content)-1:
            findNumber = content[i].find(" ")
            devices.append(content[i][0:findNumber])
            i += 1
        temp=Element(pairing, G2, value=s[2])
        print("temp=",temp)
        '''
        # B=Hash2(s[2].encode('utf-8')).hexdigest()
        B=s[2].strip()
        print("B=", B)
        cypher=[A,B] # [A,B]

        flag= peks.Test(params, pk, cypher, td)
        if(flag==1):
            ss.append(s[0]) # 将文本放入ss中
    return ss