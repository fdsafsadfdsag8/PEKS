# coding=utf-8
import time
from web3 import Web3, WebsocketProvider
from mysite.search_kw.py_files import contract_abi

contract_address= "0xfb8fe9d6b9fde5d0383b04243bcb4f6649f2aec0" # 私链地址：[YOUR CONTRACT ADDRESS]
wallet_private_key= "9bdb22597dd16ce0f81977fd85de9e9b083c1e5b63105fe7648ad04848e4de99"# [YOUR TEST WALLET PRIVATE KEY]
wallet_address= "0xe473d288faf6c2d1812dbb759d7423605c7d1a58" # 用的word里面tmf的[YOUR WALLET ADDRESS]

# 创建infura账户，参考：http://blog.hubwiz.com/2018/10/31/ethereum-python-node-windows/
# w3 = Web3(HTTPProvider("http://127.0.0.1:8000/")) #infura服务器url [YOUR INFURA URL]
# w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))# gaanche-cli仿真器
# w3 = Web3(IPCProvider()) # for an IPC based connection
w3 = Web3(WebsocketProvider('ws://127.0.0.1:8546'))

contract = w3.eth.contract(address = contract_address, abi = contract_abi.abi)

w3.eth.enable_unaudited_features() #确认我们知道可能会发生问题的情况


# 向智能合约发送以台币
def send_ether_to_contract(amount_in_ether):

    amount_in_wei = w3.toWei(amount_in_ether,'ether');
    nonce = w3.eth.getTransactionCount(wallet_address)
    txn_dict = {
            'to': contract_address, # 将以太送到哪里（在这种情况下是智能合约）
            'value': amount_in_wei, # 送多少钱，单位wei
            'gas': 2000000, # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
            'gasPrice': w3.toWei('40', 'gwei'), # 每单位gas支付多少钱（以wei为单位）
            'nonce': nonce, # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
            'chainId': 528 #每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    }
    signed_txn = w3.eth.account.signTransaction(txn_dict, wallet_private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    txn_receipt = None
    count = 0
    while txn_receipt is None and (count < 30):
        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
        print(txn_receipt)
        time.sleep(10)
    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return {'status': 'added', 'txn_receipt': txn_receipt}
'''
# 以下是调用智能合约函数的例子
def GetHuman(self,_addr):
    human = self.myContract.functions.people(self.CheckAddress(_addr)).call()
    print(human)
    
def PrintHelloWorld(self):
    mystr = self.myContract.functions.printHelloWorld().call()
    print("调用合约函数printHelloWorld结果:",mystr)
'''
#向智能合约传用户的用户名和用户的密码(交易！！)
def register(_username, _password):
    nonce = w3.eth.getTransactionCount(wallet_address)
    tx= contract.functions.register(_username, _password).buildTransaction({
        'gas': 3000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    })
    signed_tx = w3.eth.account.signTransaction(tx, wallet_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        print(tx_receipt)
    # return {'status': 'added', 'tx_receipt': tx_receipt}


# 检验用户密码是否正确，返回为bool
def fetchpwd(_username, _password):
    return contract.functions.fetchpwd(_username, _password).call()

#向智能合约传:1用户账号和密码的hash，2用户文件加密的公钥，3用户文件加密的私钥，4用户双曲线公钥，5用户双曲线私钥。(交易！！)
def newsender(_hash, _filepb, _filepv, _hyperbolapb, _hyperbolapv):
    nonce = w3.eth.getTransactionCount(wallet_address)
    tx= contract.functions.newsender(_hash, _filepb, _filepv, _hyperbolapb, _hyperbolapv).buildTransaction({
        'gas': 5000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    })
    signed_tx = w3.eth.account.signTransaction(tx, wallet_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt= w3.eth.waitForTransactionReceipt(tx_hash)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        print(tx_receipt)
    # return {'status': 'added', 'txn_receipt': tx_receipt}


# 传递用户密码与用户名的hash。返回值为string类型为对应此用户的双曲线私钥。用于接受方生成陷门
def fetchhyperpv(_hash):
    return contract.functions.fetchhyperpv(_hash).call()

#向智能合约传:1用户名，2对应的双线性公钥，为下一个函数作准备 (交易！！)
def newreceiver(_username, _pb):
    nonce = w3.eth.getTransactionCount(wallet_address)
    tx= contract.functions.newreceiver(_username, _pb).buildTransaction({
        'gas': 3000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    })
    signed_tx = w3.eth.account.signTransaction(tx, wallet_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt= w3.eth.waitForTransactionReceipt(tx_hash)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        print(tx_receipt)
    # return {'status': 'added', 'txn_receipt': tx_receipt}


# 参数为用户的用户名，返回值为string类型为用户对应双线性公钥。用于发送方关键字加密
def fetchhyperpb(_username):
    return contract.functions.fetchhyperpb(_username).call()

#向智能合约传:函数第一个参数为A，第二个参数为B,第三个参数为文件的密文。([A,B]=关键字加密) (交易！！)
def newfile(_A,_B, _cipherTEXT):
    nonce = w3.eth.getTransactionCount(wallet_address)
    tx= contract.functions.newfile(_A,_B, _cipherTEXT).buildTransaction({
        'gas': 5000000,  # gas是衡量在以太坊上执行交易的计算工作量度。指定上限。
        'gasPrice': w3.toWei('40', 'gwei'),  # 每单位gas支付多少钱（以wei为单位）
        'nonce': nonce,  # 它只是发送地址所做的先前交易次数的计数，用于防止双重花费。
        'chainId': 528  # 每个以太坊网络都有自己的链ID：主网的ID为1，而Ropsten为3
    })
    signed_tx = w3.eth.account.signTransaction(tx, wallet_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt= w3.eth.waitForTransactionReceipt(tx_hash)
    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(10)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        print(tx_receipt)
    # return {'status': 'added', 'txn_receipt': tx_receipt}


# 返回当前存储的加密文件的个数,用来for循环接收[A,B]
def fetchfilenum():
    return contract.functions.fetchfilenum().call()

# 根据上面的for循环，每次接收[A，B]，都是string类型
def fetchkeyword(i):
    return contract.functions.fetchkeyword(i).call()

# test成功之后，直接向智能合约请求对应的文件密文(每个for循环test一次)
def fetchcipher(i):
    return contract.functions.fetchkeyword(i).call()
