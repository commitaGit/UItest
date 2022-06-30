# 测试平台UI自动化

为提高测试工作效率，编写UI自动化测试平台。

## 一、目录结构

```text
├── common                 // 公共方法
├── config                 // 配置相关
├── page                   // selenium方法封装
├── PageElements           // 页面元素
├── PageObject             // 页面元素对象
├── report                 // 报告归档存放
├── script                 // 校验
├── TestCase               // 测试用例
├── TestData               // 测试数据驱动文件
└── utils                  // 工具类
```

## 二、运行项目

运行本项目，我们建议使用python的虚拟环境，与系统自身相关依赖模块隔离。下面为开发环境搭建过程。

1.软件依赖

- 本项目`python`版本为3.8以上

2.搭建运行所需的环境

python虚拟化环境官网[virtualenv](https://pypi.org/project/virtualenv)

```bash
# 首次运行该项目，需要安装。已安装可忽略。
pip3 install virtualenv
```


3.启动python虚拟环境

```bash
virtualenv .
source bin/activate
```

4.安装项目依赖

```bash
cd test-apitest
# 安装运行环境所需依赖
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip install -r requirements.txt -i https://pypi.douban.com/simple
# 启动项目
python run.py
```

5.生成依赖模块

开发完成后，需要同步项目依赖模块。

```bash
pip freeze > requirements.txt
```

【注】项目依赖模块见[requirements.txt](./requirements.txt)

6.退出python虚拟环境

```bash
deactiveate
```

### 三、如何进行测试用例的开发

1.在`TestCase`目录下新增需要编写测试功能的文件夹

按格式：TestCase_{prodcut_fuction}，如`TestCase_train`。

注：APP测试用例文件，文件名中需包含“app”（如：TestCase_app_login），便于区分是web用例和APP用例

```bash
cd test_uitest/TestCase
mkdir TestCase_train
cd TestCase_train
touch __init__.py
```

【注】可能有其他更加便利的方式，但基本上增加的基础内容如上。

2.在测试用例目录下编写相关代码

测试代码的文件名格式： test_{function}.py

例如，测试用例--后台登录是否成功

```python
# 文件名：test_admin_register.py

    def test_admin_login(self, drivers):
        """后台登录"""
        adminlogin = AdminLoginPage(drivers)
        adminlogin.get_url(ini._get("HOST", "ADMIN_LOGIN_HOST"))
        adminlogin.input_account(ADMIN_ACCOUNT)
        adminlogin.input_password(ADMIN_PASSWORD)
        adminlogin.click_login()
        assert “呼叫接入” in adminlogin.find_text()
```

## 四、TODO
