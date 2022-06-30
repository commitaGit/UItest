# 测试平台UI自动化

为提高测试工作效率，编写UI自动化测试平台。

## 一、目录结构

```text
test-uitest
├── common                // 公共方法
├── config                // 配置相关
├── page                  // selenium方法封装
├── projects              // UI自动化脚本
 |   ├── applet-uitest    // 小程序
 |   ├── h5-uitest        // h5页面
 |   ├── app-uitest       // APP端
 |   └── web-uitest       // web端
├── script                // 校验
├── README.md
├── requirements.txt      // 依赖模块
├── run.py                 
└── utils                 // 工具类
```
## 二、运行环境

- 本项目`python`版本为**3.8**以上
- [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) (本文档中简称IDE)最新版本，并打开安全模式: 设置 -> 安全设置 -> 服务端口: 打开
- 微信 >= 7.0.7 (确认微信公共库版本 >= 2.7.3即可)
- minium安装（小程序UI测试框架）
  - 自动安装：pip install https://minitest.weixin.qq.com/minium/Python/dist/minium-latest.zip
  - 手动安装：下载[minium安装包](https://minitest.weixin.qq.com/minium/Python/dist/minium-latest.zip)，解压后进入文件夹，运行python setup.py install
  - 安装完成后执行：minitest -v，显示版本信息即安装成功
  - 常见问题排查：
    - 开发者工具没有自动打开, 先排查开发者工具自动化能力，进行环境检查
      - "path/to/cli" auto --project "path/to/project" --auto-port 9420
    - 配置了真机环境但无法拉起真机上的小程序，排查是否使用了真机调试2.0, 如果是，切换回真机调试1.0
    - 报错traceback中有出现 _miniClassSetUp 的调用，确认下开发者工具上选用的基础库是最新的: 开发者工具项目窗口右上角 -> 详情 -> 本地设置 -> 调试基础库

## 三、运行项目

运行本项目，我们建议使用python的虚拟环境，与系统自身相关依赖模块隔离。下面为开发环境搭建过程。

1.搭建运行所需的环境

python虚拟化环境官网[virtualenv](https://pypi.org/project/virtualenv)

```bash
# 首次运行该项目，需要安装。已安装可忽略。
pip3 install virtualenv
```


2.启动python虚拟环境

```bash
virtualenv .
source bin/activate
```

3.安装项目依赖

```bash
cd test-apitest
# 安装运行环境所需依赖
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip install -r requirements.txt -i https://pypi.douban.com/simple
# 启动项目，运行每个UI自动化包中的文件run.py即可
eg:
cd /projects/web-uitest
python run.py
```

4.生成依赖模块

开发完成后，需要同步项目依赖模块。

```bash
pip freeze > requirements.txt
```

【注】项目依赖模块见[requirements.txt](./requirements.txt)

5.退出python虚拟环境

```bash
deactiveate
```

## 四、TODO
