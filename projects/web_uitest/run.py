import sys
import os
runpath =os.path.abspath('../..')
sys.path.append(runpath)
import pytest
from utils.times import dt_strftime



def main():
    """运行pytest命令启动测试"""
    report_name = "{}.html".format(dt_strftime("%Y%m%d"))
    pytest.main(['-v',
                 '-s',
                 '--reruns=1',
                 r'testcase',
                 '--capture=sys',
                 '--html=report/{}'.format(report_name),
                 '--self-contained-html'])

if __name__ == '__main__':
    main()

