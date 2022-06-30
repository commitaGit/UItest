from functools import wraps
import unittest
from minium import logger

testCaseName = {}

class CaseDependency:
    """
    :name:被依赖的用例名称
    :depend:依赖的用例名称
    =======example=======
    @decRelation(name='test_01')
    def test_01(self):
        self.assertEqual(2, 2)

    @decRelation(depend='test_01')
    def test_02(self):
        self.assertEqual(1, 2)
    """
    def __init__(self, name=None, depend=None):
        self.depend = depend
        self.name = name
        super(CaseDependency, self).__init__()
    # 共6种情况：
    # 1、只有name
    # 2、有name，有depend（pass）
    # 3、有name，有depend（fail）
    # 4、只有depend（pass）
    # 5、只有depend（fail）
    # 6、没有name和depend
    def __call__(self, func):
        @wraps(func)
        def decoration(*args, **kwargs):
            logger.info("testCaseName(start):", testCaseName)
            if self.name:
                testCaseName[self.name] = False  # 初始化为False，运行成功改为True
                if self.depend and testCaseName[self.depend] is True:#有name和depend,depend为pass
                    func(*args, **kwargs)
                    testCaseName[self.name] = True
                if self.depend and testCaseName[self.depend] is not True:#有name和depend,depend为fail
                    unittest.TestCase().skipTest(reason="%s 测试用例执行失败，相关依赖用例跳过!!!" % (self.depend))
                    testCaseName[func.__name__] = 'Skip'
                elif self.depend is None: # 只有name
                    func(*args, **kwargs)
                    testCaseName[self.name] = True
            if not self.name:
                if self.depend and testCaseName[self.depend] is True:#只有depend,depend为pass
                    func(*args, **kwargs)
                    testCaseName[self.name] = True
                if self.depend and testCaseName[self.depend] is not True:#只有depend,depend为fail
                    unittest.TestCase().skipTest(reason="%s 测试用例执行失败，相关依赖用例跳过!!!" % (self.depend))
                    testCaseName[func.__name__] = 'Skip'
                if not self.depend: #没有name，没有depend
                    func(*args, **kwargs)
                    testCaseName[func.__name__] = True
            logger.info("testCaseName(end):", testCaseName)
        return decoration