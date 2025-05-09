# 介绍
利用大模型帮助您进行一些简单的任务。

# 工作流程
本项目建议使用两种大模型，一种擅长语言推理能力，即`setting_template.json`文件中的`model chat`，另一种只需要支持函数调用功能即可，即`setting_template.json`文件中的`model func_call`。
在用户发送要求后，chat model 会将任何解析为“单元指令”，并逐个将指令发送给func call model。func call model接收到指令后会调用相应的函数进行执行，项目会将执行完后的结果返回给chat model。chat model会根据结果进行进一步的处理。

# 快速开始
首先，您需要准备python环境。在命令行中使用：
```
python --version
```
来查看您是否下载好python，推荐使用最新的版本
接下来将项目拉取到本地，在命令行中使用：
```
git clone git@github.com:math-zhuxy/AI-Agent.git
```
随后安装需要的python库，使用：
```
pip install -r requirements.txt
```
随后，你需要找到您的bing cookie。
方法为：打开bing浏览器，按下f12进入开发者模式，随便选择一个进行搜索
查看网络那一栏，随便选择一个数据，点击标头，找到请求表标头中的cookie字段
当然如果您觉得麻烦，这一步也可以跳过，不过可能会造成爬虫失败。
最后，运行项目，使用：
```
python main.py
```