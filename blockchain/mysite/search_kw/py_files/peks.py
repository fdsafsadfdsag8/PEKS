# coding=utf-8
# 官方用例：https://github.com/debatem1/pypbc/blob/master/test.py
# pbc官方文档: https://crypto.stanford.edu/pbc/manual/ch04s07.html
from pypbc import *
import hashlib

Hash1 = hashlib.sha256
Hash2 = hashlib.sha256

stored_params = """type a
q 8780710799663312522437781984754049815806883199414208211028653399266475630880222957078625179422662221423155858769582317459277713367317481324925129998224791
h 12016012264891146079388821366740534204802954401251311822919615131047207289359704531102844802183906537786776
r 730750818665451621361119245571504901405976559617
exp2 159
exp1 107
sign1 1
sign0 1
"""
params=Parameters(param_string = stored_params) #把参数固定下来！不然每次都会不同
pairing = Pairing(params) # 实例化双线性对对象，也就是经常表示的e(a,b)
g = Element.random(pairing, G2)
# 公钥可搜索加密-2004-Boneh,各种参数取值参考的官方文档

# 密钥生成算法，输入安全参数qbits和rbits，返回[params, g, pk, sk]
def KeyGen(qbits=512, rbits=160):
    # params = Parameters(qbits=qbits, rbits=rbits)

    # print("params=",params)


    sk = Element.random(pairing, Zr) #g和h的阶都是r
    pk = Element(pairing, G2, value=g ** sk)
    return [params, g, sk, pk]


# PEKS算法，输入公共参数[params, g]，公钥pk，关键字word，返回[A, B] （具体参考论文）
def PEKS(params, g, pk, word):
    # pairing = Pairing(params)
    word = str(word).strip()
    hash_value = Element.from_hash(pairing, G1, Hash1(word.encode('utf-8')).hexdigest())
    r = Element.random(pairing, Zr)
    temp = pairing.apply(hash_value, pk ** r)
    temp = str(temp).strip()
    # return [g**r,temp] #这里修改一下，先不返回B，这样字符串转element的时候方便
    return [g ** r, Hash2(temp.encode('utf-8')).hexdigest()]


# 陷门生成算法，输入公共参数[params]，私钥sk，待查关键字word，返回陷门td
def Trapdoor(params, sk, word):
    pairing = Pairing(params)
    word = str(word).strip()
    hash_value = Element.from_hash(pairing, G1, Hash1(word.encode('utf-8')).hexdigest())
    return hash_value ** sk


# 测试算法，输入公共参数[params]，公钥pk，S=[A, B]，陷门td，返回布尔值True/False
def Test(params, pk, cipher, td):
    pairing = Pairing(params)
    print("pairing=", pairing)
    [A, B] = cipher
    td = Element(pairing, G1, value=str(td))
    temp = pairing.apply(td, A)
    temp=str(temp).strip()
    temp = Hash2(temp.encode('utf-8')).hexdigest()
    print("Temp=", temp)
    # 如果两个字符串末尾有其他符号，比如回车‘\n’，print的时候无法发现的，所以需要strip
    a = temp.strip()
    b = B.strip()
    print(temp,B)
    print("-------------------------------------------------------------------")
    return a == b #这里修改了一下，直接比较字符串
    # return temp == B


if __name__ == '__main__':
    [params, g, sk, pk] = KeyGen(512, 160)
    # print(type(sk))
    cipher = PEKS(params, g, pk, "GQW")
    td = Trapdoor(params, sk, "GQW")
    assert(Test(params, pk, cipher, td)) # 断言，在条件为假时会抛出异常
    td = Trapdoor(params, sk, "GQK")
    assert(not Test(params, pk, cipher, td))