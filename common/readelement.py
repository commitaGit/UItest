import os
import yaml
from config.conf import cm

PATH_DICT = {"web": cm.WEB_ELEMENT_PATH,
            "app":cm.APP_ELEMENT_PATH,
            "applet":cm.APPLET_ELEMENT_PATH,
            "h5":cm.H5_ELEMENT_PATH}

class Element(object):
    """获取元素"""

    def __init__(self, channel, name):
        self.file_name = '%s.yaml' % name
        self.element_path = os.path.join(PATH_DICT[channel], self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("%s 文件不存在！" % self.element_path)
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item):
        """获取属性"""
        data = self.data.get(item)
        if data:
            name, value = data.split('==')
            return name, value
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))


if __name__ == '__main__':
    search = Element('web','web_register')
