import random
import utils.constant as const
from datetime import datetime, timedelta

def generate_id():
   """ 随机生成身份证号，sex = 0表示女性，sex = 1表示男性 """

   sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
   # 随机生成一个区域码(6位数)
   id_number = str(random.choice(list(const.AREA_INFO.keys())))
   # 限定出生日期范围(8位数)
   start, end = datetime.strptime("1960-01-01", "%Y-%m-%d"), datetime.strptime("2000-12-30", "%Y-%m-%d")
   birth_days = datetime.strftime(start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d")
   id_number += str(birth_days)
   # 顺序码(2位数)
   id_number += str(random.randint(10, 99))
   # 性别码(1位数)
   id_number += str(random.randrange(sex, 10, step=2))
   # 校验码(1位数)
   return id_number + str(get_check_digit(id_number))

def get_check_digit(id_number):
    """ 通过身份证号获取校验码 """
    check_sum = 0
    for i in range(0, 17):
        check_sum += ((1 << (17 - i)) % 11) * int(id_number[i])
    check_digit = (12 - (check_sum % 11)) % 11
    return check_digit if check_digit < 10 else 'X'

if __name__ == '__main__':
    print(generate_id())  # 随机生成身份证号
