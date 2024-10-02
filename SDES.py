from Function_f import Function_f
from SW import SW
from IP import IP
from SubKeyGenerator import SubKeyGenerator
import numpy as np
'''
C = IP^{-1}(f_{k2}(SW(f_{k1}(IP(P)))))
P = IP^{-1}(f_{k1}(SW(f_{k2}(IP(C)))))
'''
class SDES:
    def __init__(self):
        self.ip = IP()
        self.sw = SW()
        self.function_f = Function_f()
        self.subkeygenerator = SubKeyGenerator()

    # type == 'C' : text是明文
    # type == 'P' : text是密文
    def encryptOrDecrypt(self, text, key, type):
        # 生成子密钥k1和k2
        k1 = self.subkeygenerator.generate(key, 1)
        k2 = self.subkeygenerator.generate(key, 2)

        # 初始置换IP
        text = self.ip.initialP(text)

        # 第一次轮函数计算(加密和解密只有f_{k1}和f_{k2}的使用顺序不同)
        if type == 'C':
            text = self.function_f.calculate(text, k1)
        else:
            text = self.function_f.calculate(text, k2)

        # SW
        text = self.sw.swap(text)

        # 第二次轮函数计算(加密和解密只有f_{k1}和f_{k2}的使用顺序不同)
        if type == 'C':
            text = self.function_f.calculate(text, k2)
        else:
            text = self.function_f.calculate(text, k1)

        # 逆初始置换IP^{-1}
        text = self.ip.initialP_Inverse(text)  # 初始置换

        if type == 'C':
            print("加密结果为:", text)
        else:
            print("解密结果为:", text)

        return text

if __name__ == "__main__":
    # c = np.array([1,0,0,1 ,0,0,1,1])
    # key = np.array([0,1,1,0,1,1,0,1,0,0])

    c = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    key = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    sdes = SDES()
    p = sdes.encryptOrDecrypt(c, key, 'C')
    print("密文:", p)