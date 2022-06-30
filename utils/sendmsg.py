import requests
import json


class sendmsg:

    def send_msg(self, msg):
        msg = {"msgtype": "text", "text": {"content": msg}}
        data= json.dumps(msg)
        waring_basehttp = requests.post(url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55e178d6-9132-4dbc-a251-d34931063fd3',
                                        headers={'Content-Type': 'application/json'},data=data)


if __name__ == '__main__':
    sendmsg().send_msg("测试用例执行结束:%s  \n" % 1 + \
                          "**********开始打印结果********** \n" + \
                          "总运行测试用例数:%d \n" % 2 + \
                          "通过测试用例数:%d \n" % 3 + \
                          "跳过用例数:%d \n" % 4 + \
                          '失败的测试用例数:%d \n' % 5 + \
                          "错误用例数:%d \n" % 6 + \
                          "运行总时间:%s\n" % 7)