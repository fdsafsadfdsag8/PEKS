# 基于关键字加密搜索的信息传递系统1.0

## 1环境

- ubuntu系统
- python3.0
- pycharm软件
- pypbc库
- django框架
- 以太坊

## 2安装方法

- pypbc库：

  [Ubuntu安装pypby](https://blog.csdn.net/KoalaZB/article/details/89499048)

- django：

	- 安装pip3：sudo apt-get install python3-pip

	- 安装django：sudo pip3 install django

	- 检验是否已安装好：

  ```python
  python3
  >>>import django
  >>>django.get_version()
  ```

- web3.py：

  [Ubuntu安装web3.py](https://www.jianshu.com/p/7bdf432890ad)

- 以太坊私链：见相关文档 和 [Windows下使用python-web3.py进行以太坊Dapp开发](https://www.mscto.com/blockchain/258474.html)

## 3使用步骤

### 3.1布置智能合约

- 按照文档：《部署合约并调用智能合约的函数》和《私链上合约的相关信息和函数5.0》

### 3.2创建本地文件夹

- 在本地创建文件夹(如命名为test)
- 在test里面创建两个文件夹：privkey和pubkey


### 3.3修改代码

- 安装狐狸钱包获取钱包私钥，参考教程：

  - [MetaMask安装使用指南](https://blog.csdn.net/Fly_hps/article/details/104115231?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-5.nonecase&amp;depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-5.nonecase)

  - [连接私有节点并导入节点账号](https://blog.csdn.net/weixin_35282902/article/details/82916908)

  - ps：注意url我们的端口号用的4444

- 用pycharm打开blockchain_demo文件夹，修改search_kw文件夹下的view.py：
	
	- 将开头的两个变量：wallet_private_key 和wallet_address 修改为自己对应的钱包私钥和钱包地址
	- 将函数signup2里的 path = ''  修改为上述创建的test文件夹路径xx/test   (注意没有最后的下划线)

### 3.4启动程序
- 启动区块链
- 在pycharm终端的blockchain_demo/mysite$目录下：python manage.py runserver
- 进入网址
- 输入后缀url即可访问对应网页

## 4注意事项

- 在注册之后必须进行挖矿
- 在发送信息之后也必须进行挖矿

