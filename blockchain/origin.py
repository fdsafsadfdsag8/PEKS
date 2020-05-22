# coding=utf-8
# 这是最简单的版本，将整个流程串起来
# 保存信息到本地文件，需要的时候直接从本地读取。（暂时没有智能合约的参与）

import base64
from mysite.search_kw.py_files import peks, msg
import search
import upload
import rsa
from pypbc import *

if __name__ == '__main__':

    [params, g, sk, pk]= peks.KeyGen(512, 160)

    pubkey, privkey = msg.create_key()
    # 先生成一对密钥，然后保存.pem格式文件，当然也可以直接使用
    # (pubkey, privkey) = rsa.newkeys(1024)

    pub = pubkey.save_pkcs1()
    pubfile = open('public.pem', 'wb')
    pubfile.write(pub)
    pubfile.close()

    pri = privkey.save_pkcs1()
    prifile = open('private.pem', 'wb')
    prifile.write(pri)
    prifile.close()

    # load公钥和密钥
    message = 'lovesoo.org'
    message.encode("utf-8")
    with open('public.pem') as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)

    with open('private.pem') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)

    # 用公钥加密、再用私钥解密
    crypto = msg.rsaEncrypt(message, pubkey)
    message = msg.rsaDecrypt(crypto, privkey)
    print(message)

    print("pk=",pk)
    print("sk=", sk)
    pairing = Pairing(params)
    sk_str = repr(sk)
    print("type=",type(sk_str))
    # sk_str = str(sk).decode('hex')
    #skk=eval(sk_str)
    sk_hex=eval(sk_str) # 还原
    sk_int=int(sk_hex)
    print("type=", type(sk_int))
    print("sk_int=", sk_int)
    skk = Element(pairing, Zr,value=sk_int)  # g和h的阶都是r
    pk_str=str(pk).strip()
    pkk = Element(pairing, G2, value=pk_str)
    print("pk=",pkk)
    print("sk=", skk)


    for i in range(5):
        # 输入字符串信息，进行加密
        text=input("请输入上传的明文信息:\n")
        en_text= msg.rsaEncrypt(text, pubkey)
        print(en_text)

        # 输入一个关键字，对关键字加密
        w=input("请输入对应关键字:\n")
        [A, B]= peks.PEKS(params, g, pk, w)
        cypher=[A,B]
        print(cypher)

        # 保存上述信息到本地文件,创建文件，写入信息
        upload.write_in_txt(en_text, cypher)

        # 输入需要查询的关键字进行查询，生成陷门
        q_w = input("请输入需要查询的关键字:\n")
        td= peks.Trapdoor(params, sk, q_w)

        # 扫描本地目录下的文件，进行匹配
        ss= search.sh(params, pk, td)

        l=len(ss) #获取列表长度
        if(l!=0):
            # 匹配成功，则返回加密后的信息,信息解密并打印
            for s in ss:
                b = base64.decodestring(s.encode('utf-8'))
                de_text = msg.rsaDecrypt(b, privkey) # 将字符串转为byte
                print(de_text)
        else:
            # 匹配失败则打印失败信息
            print("未找到任何信息！\n")
