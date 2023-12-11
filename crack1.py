import time
from typing import List
from tqdm import tqdm
from itertools import chain
from zipfile import ZipFile
import zipfile
"""
单线程生成密码，单线程尝试
"""

start = time.time()

# chr(97) -> 'a' 这个变量保存了密码包含的字符集
dictionaries = [chr(i) for i in
                chain(range(97, 123),    # a - z
                      range(65, 91),    # A - Z
                      range(48, 58))]    # 0 - 9

#dictionaries.extend(['.com', 'www.'])    # 添加自定义的字符集

file_name ='./john.zip' # 你的文件路径

def all_passwd(dictionaries: List[str], maxlen: int):
    # 返回由 dictionaries 中字符组成的所有长度为 maxlen 的字符串

    def helper(temp: list, start: int, n: int):
        # 辅助函数，是个生成器
        if start == n:    # 达到递归出口
            yield ''.join(temp)
            return
        for t in dictionaries:
            temp[start] = t    # 在每个位置
            yield from helper(temp, start + 1, n)

    yield from helper([0] * maxlen, 0, maxlen)

#zfile = ZipFile(file_name, 'r')    # 很像open

def extract(pwd: str) -> bool:
    # zfile: 一个ZipFile类, pwd: 密码

    with zipfile.ZipFile(file_name, 'r') as zip_file:
        try:
            zip_file.extractall(pwd=bytes(pwd, 'utf-8'))    # 密码输入错误的时候会报错
            now = time.time()                                      # 故使用 try - except 语句
            print(f"Password is: {pwd}")                           # 将正确的密码输出到控制台
            return True
        except:
            pass
        
    return False    
# 用 bool 类型的返回值告诉主程序是否破解成功 (意思就是返回 True 了以后就停止)

lengths = [2, 3, 4,5,6,7,8]    # 密码长度
total = sum(len(dictionaries) ** k for k in lengths)    # 密码总数


for pwd in tqdm(chain.from_iterable(all_passwd(dictionaries, maxlen) for maxlen in lengths), total=total):
    if extract(pwd):    # 记得extract函数返回的是bool类型的哦
        break