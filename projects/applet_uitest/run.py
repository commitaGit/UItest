import os, shutil
import time
import unittest
from unittestreport import TestRunner

if __name__ == '__main__':
    # # 清除之前的测试报告
    # if os.path.exists("outputs"):
    #     shutil.rmtree("outputs")
    # 测试用例目录
    base_path = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(base_path, "testcase")
    # 加载测试用例
    discover = unittest.defaultTestLoader.discover(test_dir, 'test_*.py')  # 返回值是一个测试套件
    runner = TestRunner(suite=discover, desc="小程序UI自动化测试报告")
    runner.rerun_run(count=1)  # 所有用例失败重试
    time.sleep(3)
    # # 输出测试报告
    # if os.path.exists("report"):
    #     shutil.rmtree("report")
    # os.system('minireport outputs report')
    # time.sleep(2)
    # # 启动本地服务，并映射报告文件
    # os.system('python -m http.server 8080 -d report')


