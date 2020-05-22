# coding=utf-8
# 包含一个大的JSON信息字符串，Python需要与智能合约中定义的函数进行交互，称为应用程序二进制接口（ABI）。
# 可以在Remix中找到智能合约的ABI的JSON字符串
# http://blog.hubwiz.com/2018/12/14/ethereum-python-smartcontract/
# https://www.mscto.com/blockchain/258474.html

abi = '''
[{\"constant\":true,\"inputs\":[{\"name\":\"_username\",\"type\":\"string\"}],\"name\":\"fetchmsgpb\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_hash\",\"type\":\"string\"}],\"name\":\"fetchmsgpv\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_hash\",\"type\":\"string\"}],\"name\":\"fetchhyperpv\",\"outputs\":[{\"name\":\"\",\"type\":\"int256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_hash\",\"type\":\"string\"},{\"name\":\"_filepb\",\"type\":\"string\"},{\"name\":\"_filepv\",\"type\":\"string\"},{\"name\":\"_hyperbolapb\",\"type\":\"string\"},{\"name\":\"_hyperbolapv\",\"type\":\"int256\"}],\"name\":\"newsender\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_username\",\"type\":\"string\"},{\"name\":\"_hyperbolapb\",\"type\":\"string\"},{\"name\":\"_filepb\",\"type\":\"string\"}],\"name\":\"newreceiver\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_username\",\"type\":\"string\"}],\"name\":\"fetchhyperpb\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"fetchfilenum\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_keyworda\",\"type\":\"string\"},{\"name\":\"_keywordb\",\"type\":\"string\"},{\"name\":\"_cipher\",\"type\":\"string\"}],\"name\":\"newfile\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"i\",\"type\":\"uint256\"}],\"name\":\"fetchkeyword\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"},{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"i\",\"type\":\"uint256\"}],\"name\":\"fetchcipher\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"}]
'''