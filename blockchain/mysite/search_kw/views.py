# coding=utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms

import time
import datetime
import base64
import rsa
from pypbc import *
from web3 import Web3, WebsocketProvider,Account
from .py_files import peks, msg
import hashlib

Hash1 = hashlib.sha256

from .py_files import contract_abi

contract_address = "0xD2298de9799a81f38CDEC9524Eb93d1bc2488EB8"# 私链地址：[YOUR CONTRACT ADDRESS]
# wallet_private_key= '9bdb22597dd16ce0f81977fd85de9e9b083c1e5b63105fe7648ad04848e4de99'# [YOUR TEST WALLET PRIVATE KEY]
wallet_private_key = "ed2454d8e3c219039b3299ff10ba528fc94cdff1208c19bc5fbc81026f4970a9" # 狐狸钱包
wallet_address = "0x8411f3782775aca8be8adfb625047ea852d4b79b"  # 用的word里面tmf的[YOUR WALLET ADDRESS]

# 创建infura账户：http://blog.hubwiz.com/2018/10/31/ethereum-python-node-windows/
# w3 = Web3(HTTPProvider("http://127.0.0.1:8000/")) #infura服务器url [YOUR INFURA URL]
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:4444'))
# w3 = Web3(IPCProvider()) # for an IPC based connection
# w3 = Web3(WebsocketProvider('ws://127.0.0.1:8546'))
contract_address = w3.toChecksumAddress(contract_address)
wallet_address = w3.toChecksumAddress(wallet_address)

contract = w3.eth.contract(address = contract_address, abi = contract_abi.abi)
# account=Account.create(123456)
# w3.eth.enable_unaudited_features() #确认我们知道可能会发生问题的情况
un='' #记录本次登陆的用户名
pw='' #记录本次登陆的密码
g=peks.g
nonce= w3.eth.getTransactionCount(wallet_address)
params=peks.params
pairing=peks.pairing
sh_flag=0
data = []  # 存获取的密文文件

def index(request):
    pass
    return render(request, 'index.html')
    '''
    render方法接收request作为第一个参数，要渲染的页面为第二个参数，
    
    需要传递给页面的数据字典作为第三个参数（可以为空），表示根据请求的部分，以渲染的HTML页面为主体，
    使用模板语言将数据字典填入，然后返回给用户的浏览器。
    '''
    # return HttpResponse("Hello, world. You're at the search_kw index.")

def index2(request):
    global un
    global pw
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                # Python内置了一个locals()函数，它返回当前所有的本地变量字典
                return render(request, 'index2.html', locals())

            if user.password == password:
                un = username
                pw = password
                return redirect('/sendRcv2/')
            else:
                message = '密码不正确！'
                # return render(request, 'index_new.html', {'message': message}) # 用于保存提示信息，还需要对login.html进行修改才能在前端显示
                return render(request, 'index2.html', locals())
        else:
            return render(request, 'index2.html', locals())
    return render(request, 'index2.html', locals())



def index_new(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                # Python内置了一个locals()函数，它返回当前所有的本地变量字典
                return render(request, 'index_new.html', locals())

            if user.password == password:
                un=username
                pw=password
                return redirect('/sendRcv/')
            else:
                message = '密码不正确！'
                # return render(request, 'index_new.html', {'message': message}) # 用于保存提示信息，还需要对login.html进行修改才能在前端显示
                return render(request, 'index_new.html', locals())
        else:
            return render(request, 'index_new.html', locals())
    return render(request, 'index_new.html', locals())

def signup2(request):
    global nonce
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(username,password1)
        message = '请检查填写的内容！'
        if username.strip() and password1 :
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'signup2.html', locals())
            same_name_user = models.User.objects.filter(name=username)
            if same_name_user:
                message = '用户名已经存在'
                return render(request, 'signup2.html', locals())

            # 保存到数据库
            new_user = models.User()
            new_user.name = username
            new_user.password = password1
            new_user.save()

            # 给合约发点钱
            # send_ether_to_contract(0.03)
            # print(w3.eth.getBalance(wallet_address))

            # 注册时生成文件的密钥和双曲线密钥并传给智能合约
            [param, _g, sk, pk] = peks.KeyGen(512, 160)
            pubkey, privkey = msg.create_key()
            params=param
            g=_g
            u_p_word=username+password1
            _hash=Hash1(u_p_word.encode('utf-8')).hexdigest()

            #(<class 'str'>,
            # < class 'rsa.key.PublicKey' >,
            # < class 'rsa.key.PrivateKey' >,
            # < class 'pypbc.Element' >,
            # < class 'pypbc.Element' > )
            # pubkey, privkey这里传递的是对应文件名,文件存在本地
            path = '/home/savoki/test_origin'  # 设置文件夹路径
            str1 = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # 获取当前时间并转化成字符串,作为文件名
            filename1 = path + "/pubkey/" + str1 + '.pem'
            pubkey_fn=str1 + '.pem'
            pub = pubkey.save_pkcs1()
            pubfile = open(filename1, 'wb')
            pubfile.write(pub)
            pubfile.close()

            str2 = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # 获取当前时间并转化成字符串,作为文件名
            filename2 = path + "/privkey/" + str2 + '.pem'
            privkey_fn = str2 + '.pem'
            pri = privkey.save_pkcs1()
            prifile = open(filename2, 'wb')
            prifile.write(pri)
            prifile.close()

            sk_str = repr(sk)
            sk_hex = eval(sk_str)  # 还原成16进制的整数
            sk_int=int(sk_hex) # 转成int便于智能合约接收
            pk_str = str(pk).strip()

            newsender(_hash, pubkey_fn, privkey_fn, pk_str, sk_int)
            newreceiver(username, pk_str, pubkey_fn)

            nonce1 = nonce+2
            nonce = nonce1
            print(nonce)

            return redirect('/index2/')
        else:
            return render(request, 'signup2.html', locals())
    return render(request, 'signup2.html', locals())

def login(request):
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            # username.strip()中strip方法，将用户名前后无效的空格剪除
            username = login_form.cleaned_data.get('username') # get('username')中的键‘username’是HTML模板中表单的input元素里‘name’属性定义的值。
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                # Python内置了一个locals()函数，它返回当前所有的本地变量字典
                return render(request, 'login.html', locals())

            if user.password == password:
                return redirect('/index/')
            else:
                message = '密码不正确！'
                # return render(request, 'login/login.html', {'message': message}) # 用于保存提示信息，还需要对login.html进行修改才能在前端显示
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())

def sendRcv2(request):
    global nonce
    if request.method == 'POST':
        reserver = request.POST.get('reserver') #接收者的名字
        keyword = request.POST.get('keyword')
        text=request.POST.get('text')
        message = '请检查填写的内容！'
        if reserver and keyword and text:
            # 向智能合约请求，从而加密文件以及加密关键字,并将结果发回给智能合约
            pubkey_fn = fetchmsgpb(reserver)
            path = '/home/savoki/test_origin/pubkey'  # 文件夹路径
            filename = path + '/' + pubkey_fn
            print(filename)
            with open(filename) as publickfile:
                p = publickfile.read()
                pubkey = rsa.PublicKey.load_pkcs1(p)
            en_text = msg.rsaEncrypt(text, pubkey)
            string = str(base64.encodestring(en_text).decode('utf-8'))  # 把字节型转为字符串
            string = string.replace("\r", "");  # 集中成一行，便于之后按行读取
            string = string.replace("\n", "");

            pk_str=fetchhyperpb(reserver)
            pk = Element(pairing, G2, value=pk_str)

            [A, B] = peks.PEKS(params, g, pk, keyword)
            a = str(A).strip()
            b = str(B).strip()

            newfile(a, b, string)
            nonce1 = nonce + 1
            nonce=nonce1
            print(nonce)
            message = '发送成功！'

    return render(request, 'sendRcv2.html',locals())

def search2(request):
    message = ''
    global un
    global pw
    global sh_flag,data
    print("un=",un)
    print("data=",data)

    if un == '':
        message = '请先登陆！！！'
        return render(request, 'search2.html', locals())
    if request.method == 'POST':
        if sh_flag==0:
            keyword = request.POST.get('keyword')
            print(keyword)
            message = '请检查填写的内容！'
            # pairing = Pairing(params)
            if keyword:
                # 关键字生成陷门
                u_p_word = un + pw
                _hash = Hash1(u_p_word.encode('utf-8')).hexdigest()

                #sk_str=fetchhyperpv(_hash)
                #sk_hex = eval(sk_str)  # 还原
                sk_hex=fetchhyperpv(_hash)
                sk = Element(pairing, Zr, value=sk_hex)  # g和h的阶都是r

                td = peks.Trapdoor(params, sk, keyword)

                message = '未搜索到任何结果！'

                # 总文件个数
                n=fetchfilenum()
                print(n)

                # pairing = Pairing(params)
                pk_str = fetchhyperpb(un)
                pk = Element(pairing, G2, value=pk_str)

                for i in range(n):
                    [a,b]=fetchkeyword(i) #接收AB
                    A = Element(pairing, G1, value=a.strip())
                    B = b.strip()
                    cypher = [A, B]

                    flag = peks.Test(params, pk, cypher, td)
                    if flag==1:
                        en_text=fetchcipher(i) # test成功之后，直接向智能合约请求对应的文件密文
                        data.append(en_text)
                        message = '搜索完毕！'
                        content = {
                            "data": data,
                            "message":message,
                        }
                        sh_flag=1
                        return render(request, 'search2.html', content)
        if sh_flag==1:
            # 响应点击解密的事件
            data_de=[]
            message = '明文返回完毕！'
            u_p_word = un + pw
            _hash = Hash1(u_p_word.encode('utf-8')).hexdigest()
            # 解密
            privkey_fn=fetchmsgpv(_hash)
            print("privkey_fn=",privkey_fn)
            path = '/home/savoki/test_origin/privkey'  # 文件夹路径
            filename=path+'/'+privkey_fn
            with open(filename) as privatefile:
                p = privatefile.read()
                privkey = rsa.PrivateKey.load_pkcs1(p)

                for s in data:
                    b = base64.decodestring(s.encode('utf-8'))
                    de_text = msg.rsaDecrypt(b, privkey)  # 将字符串转为byte
                    data_de.append(de_text)
            content = {
                "data": data,
                "data_de": data_de,
                "message":message,
            }
            sh_flag=0
            data=[]
            return render(request, 'search2.html', content)
        else:
            return render(request, 'search2.html',locals())

    return render(request, 'search2.html',locals())

def search_test(request):
    # posts=调用函数，从而和智能合约交互
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        message = '请检查填写的内容！'
        data = []  # 存获取的密文文件
        # pairing = Pairing(params)
        if keyword:
            # 关键字生成陷门
            u_p_word = un + pw
            _hash = Hash1(u_p_word.encode('utf-8')).hexdigest()

            sk_hex=fetchhyperpv(_hash)
            sk = Element(pairing, Zr, value=sk_hex)  # g和h的阶都是r

            td = peks.Trapdoor(params, sk, keyword)

            message = '未搜索到任何结果！'

            # 总文件个数
            n=fetchfilenum()

            # pairing = Pairing(params)
            pk_str = fetchhyperpb(un)
            pk = Element(pairing, G2, value=pk_str)

            for i in range(n):
                [a,b]=fetchkeyword(i) #接收AB
                A = Element(pairing, G1, value=a.strip())
                B = b.strip()
                cypher = [A, B]

                flag = peks.Test(params, pk, cypher, td)
                if flag==1:
                    en_text=fetchcipher(i) # test成功之后，直接向智能合约请求对应的文件密文
                    data.append(en_text)
                    message = '搜索完毕！'
            #data=['asdasdsadsa','hhhhhhhhhhhhh','sbsbsbsbsbsbbs']
            content={
                # "posts":"hello world!",
                "data":data,
            }
            a=fetchhyperpv("tmf123456")
            print(a)
            print(w3.eth.getBalance( wallet_address))
            n=fetchfilenum()
            print(n)
            cc="zzx"
            pubkey_fn = fetchmsgpb(cc)
            print("filename=",pubkey_fn)

            return render(request, 'search_test.html', content)


    # 给合约发点钱
    #dicresult = send_ether_to_contract(0.0003)
    #print(dicresult)
    # wallet_privkey=account.privateKey
    # waddress=account.address

    return render(request, 'search_test.html', locals())


# 向智能合约发送以台币
def send_ether_to_contract(amount_in_ether):# 单位是eth而不是wei.
    amount_in_wei = w3.toWei(amount_in_ether, 'ether');
    nonce = w3.eth.getTransactionCount(wallet_address)
    txn_dict = {
        'to': contract_address,  # 将以太送到哪里（在这种情况下是智能合约）
        'value': amount_in_wei,  # 送多少钱，单位wei
        'gas': 2000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    }
    print(w3.eth.getBalance(wallet_address))
    signed_txn = w3.eth.account.signTransaction(txn_dict,private_key= wallet_private_key)
    print("w3.eth.getBalance(wallet_address)")
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(w3.eth.getBalance(wallet_address))
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    count = 0
    while txn_receipt is None and (count < 30):
        time.sleep(10)
        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
        print(txn_receipt)
    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return {'status': 'added', 'txn_receipt': txn_receipt}


# 向智能合约传:1用户账号和密码的hash，2用户文件加密的公钥，3用户文件加密的私钥，4用户双曲线公钥，5用户双曲线私钥。(交易！！)
def newsender(_hash, _filepb, _filepv, _hyperbolapb, _hyperbolapv):
    # nonce = w3.eth.getTransactionCount(wallet_address)
    tx = contract.functions.newsender(_hash, _filepb, _filepv, _hyperbolapb, _hyperbolapv).buildTransaction({
        'value': 0,
        'gas': 3000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    })
    signed_tx = w3.eth.account.signTransaction(tx, private_key=wallet_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash
    #tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #count = 0
    #while tx_receipt is None and (count < 30):
    #    time.sleep(10)
    #    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    #    print(tx_receipt)
    # return {'status': 'added', 'txn_receipt': tx_receipt}


# 传递用户密码与用户名的hash。返回值为string类型为对应此用户的双曲线私钥。用于接受方生成陷门
def fetchhyperpv(_hash):
    return contract.functions.fetchhyperpv(_hash).call()
# 传递用户密码与用户名的hash。返回值为string类型为对应此用户的文件私钥。用于最后自己解密
def fetchmsgpv(_hash):
    return contract.functions.fetchmsgpv(_hash).call()


# 向智能合约传:1用户名，2对应的双线性公钥，3文件的公钥，为下一个函数作准备 (交易！！)
def newreceiver(_username, _pb,_msgpb):
    # nonce = w3.eth.getTransactionCount(wallet_address)
    tx = contract.functions.newreceiver(_username, _pb,_msgpb).buildTransaction({
        'value':0,
        'gas': 3000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce+1,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    })
    signed_tx = w3.eth.account.signTransaction(tx, private_key= wallet_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash
    #tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #count = 0
    #while tx_receipt is None and (count < 30):
    #    time.sleep(10)
    #    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    #   print(tx_receipt)
    # return {'status': 'added', 'txn_receipt': tx_receipt}


# 参数为用户的用户名，返回值为string类型为用户对应双线性公钥。用于发送方关键字加密
def fetchhyperpb(_username):
    return contract.functions.fetchhyperpb(_username).call()
# 参数为用户的用户名，返回值为string类型为用户对应文件公钥。用于发送方文件加密
def fetchmsgpb(_username):
    return contract.functions.fetchmsgpb(_username).call()


# 向智能合约传:函数第一个参数为A，第二个参数为B,第三个参数为文件的密文。([A,B]=关键字加密) (交易！！)
def newfile(_A, _B, _cipherTEXT):
    # nonce = w3.eth.getTransactionCount(wallet_address)
    tx = contract.functions.newfile(_A, _B, _cipherTEXT).buildTransaction({
        'value': 0,
        'gas': 3000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    })
    signed_tx = w3.eth.account.signTransaction(tx, wallet_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash
    #tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #count = 0
    #while tx_receipt is None and (count < 30):
    #    time.sleep(10)
    #    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    #    print(tx_receipt)
    # return {'status': 'added', 'txn_receipt': tx_receipt}


# 返回当前存储的加密文件的个数,用来for循环接收[A,B]
def fetchfilenum():
    return contract.functions.fetchfilenum().call()


# 根据上面的for循环，每次接收[A，B]，都是string类型
def fetchkeyword(i):
    return contract.functions.fetchkeyword(i).call()


# test成功之后，直接向智能合约请求对应的文件密文(每个for循环test一次)
def fetchcipher(i):
    return contract.functions.fetchcipher(i).call()
