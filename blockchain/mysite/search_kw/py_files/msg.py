# coding=utf-8
# 对明文进行加解密操作 https://blog.csdn.net/whatday/article/details/97617461
# rsa保存：https://www.cnblogs.com/52python/p/6589869.html
import rsa

# rsa加密
def rsaEncrypt(str,pubkey):
    # 明文编码格式
    content = str.encode("utf-8")
    # 公钥加密
    crypto = rsa.encrypt(content, pubkey)
    return crypto

# rsa解密
def rsaDecrypt(str,pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    con = content.decode("utf-8")
    return con

def create_key():
    # 生成公钥、私钥
    (pubkey, privkey) = rsa.newkeys(512)
    # print("公钥:\n%s\n私钥:\n%s" % (pubkey, privkey))
    return (pubkey,privkey)

if __name__ == "__main__":
    s=input("input:\n")
    pubkey, privkey=create_key()
    en_str= rsaEncrypt(s,pubkey)
    print("加密后密文：\n%s" % en_str)
    content = rsaDecrypt(en_str, privkey)
    print("解密后明文：\n%s" % content)