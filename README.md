# 基于关键字加密搜索的信息传递系统1.0

## 1 环境

- ubuntu系统
- python3.0
- pycharm软件
- pypbc库
- django框架
- 以太坊

## 2 安装方法

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

## 3 使用步骤

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
	
	- 将开头的变量：contract_address 改成合约部署的地址
	- 接下来两个变量：wallet_private_key 和wallet_address 修改为自己对应的钱包私钥和钱包地址
	- 将函数signup2里的 path = ''  修改为上述创建的test文件夹路径xx/test   (注意没有最后的下划线)

### 3.4启动程序
- 启动区块链
- 在pycharm终端的blockchain_demo/mysite$目录下：python manage.py runserver
- 进入网址
- 输入后缀url即可访问对应网页

## 4 注意事项

- 在注册之后必须进行挖矿
- 在发送信息之后也必须进行挖矿

## 5 其它问题

- 关于python虚拟路径失效的问题：[PyCharm中如何导入别人的项目](https://blog.csdn.net/baidu_27922823/article/details/88233528?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase)
- 在测试链上部署相关操作：

  - [以太坊测试网络Ropsten部署智能合约](https://www.jianshu.com/p/2d5a87b81e59)
  - [Infura：一键接入以太坊](https://blog.csdn.net/TurkeyCock/article/details/85103434)

## 6 测试工具
- Apachebench：

  [性能测试工具ApacheBench](https://www.jianshu.com/p/c72402bfcca6)
