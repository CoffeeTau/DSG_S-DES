import itertools
import time

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from SDES import SDES

from utils import convert_to_np_array, convert_to_decimal, np10ToDecimal, decimalToNp10
from scipy.stats import spearmanr
from scipy.stats import ttest_rel
class StatisticalAnalysis:
    def __init__(self):
        self.sdes = SDES()  # SDES算法类

    # 产生明文-密钥-密文组，并返回十进制类型
    # num表示产生的组数
    def generateGroup(self, num):
        # 产生数据并存储
        cnt = 0
        with open('plaintext_key_ciphertext.csv', 'w') as f:
            f.write("plainText" + ',' + "key" + ',' + "cipherText" + '\n')
            while cnt < num:
                plainText = np.random.randint(0, 2, size=8)
                key = np.random.randint(0, 2, size=10)
                cipherText = self.sdes.encryptOrDecrypt(plainText, key, 'E')

                plainText_str = ''.join(str(i) for i in plainText)
                key_str = ''.join(str(i) for i in key)
                cipherText_str = ''.join(str(i) for i in cipherText)

                f.write(plainText_str + ',' + key_str + ',' + cipherText_str + '\n')

                cnt += 1

        # 读取数据并返回
        data = pd.read_csv('plaintext_key_ciphertext.csv')

        plainText = convert_to_np_array(data['plainText'].values)
        cipherText = convert_to_np_array(data['cipherText'].values)
        key = convert_to_np_array(data['key'].values)

        # 转换为十进制，方便绘制散点与进行统计分析
        plainText_decimal = convert_to_decimal(plainText)
        cipherText_decimal = convert_to_decimal(cipherText)
        key_decimal = convert_to_decimal(key)

        self.plainText_decimal = plainText_decimal
        self.cipherText_decimal = cipherText_decimal
        self.key_decimal = key_decimal

        # 可以加个判断，如果返回不为空，则数据生成成功
        return plainText_decimal, cipherText_decimal, key_decimal

    '''
    相关分析
    pair表示要探究的两个变量之间的相关性:
    1. 扩散. 明文-密文 pair == 'P-C'
    2. 混淆. 密钥-密文 pair == 'K-C'
    type表示相关分析类型(Pearson, Spearman)
    '''
    def correlationAnalysis(self, pair, type):
        if type == 'Pearson':
            if pair == 'P-C':
                correlation = np.corrcoef(self.plainText_decimal, self.cipherText_decimal)[0, 1]
            elif pair == 'K-C':
                correlation = np.corrcoef(self.key_decimal, self.cipherText_decimal)[0, 1]
            return correlation

        # 注意，Spearman的原假设是两者具有相关性
        elif type == 'Spearman':
            if pair == 'P-C':
                rho, p_value = spearmanr(self.plainText_decimal, self.cipherText_decimal)
            elif pair == 'K-C':
                rho, p_value = spearmanr(self.key_decimal, self.cipherText_decimal)
            return rho, p_value

    '''
    雪崩效应检验
    Diffusion 明文输入发生微小变化，密文输出就会截然不同
    Confusion 密钥输入发生微小变化，密文输出就会截然不同
    
    微小变化的定义: 改变二进制数组的其中一位
    截然不同的定义: 如果密文的差异位数超过密文总位数的一半, 可以认为是截然不同
    '''
    def avalancheTest(self):
        # 测试明文微小变化引起的雪崩效应（Diffusion）
        num_samples = 100
        diffusion_different_count = 0
        diffusion_total_count = 0
        for _ in range(num_samples):
            plaintext = np.random.randint(0, 2, size=8)
            key = np.random.randint(0, 2, size=10)
            original_ciphertext = self.sdes.encryptOrDecrypt(plaintext, key, 'E')

            for i in range(len(plaintext)):
                changed_plaintext = plaintext.copy()
                changed_plaintext[i] = 1 - changed_plaintext[i]
                changed_ciphertext = self.sdes.encryptOrDecrypt(changed_plaintext, key, 'E')
                different_count = np.sum(original_ciphertext!= changed_ciphertext)
                if different_count > len(original_ciphertext) / 2:
                    diffusion_different_count += 1
                diffusion_total_count += 1

        diffusion_proportion = diffusion_different_count / diffusion_total_count

        # 测试密钥微小变化引起的雪崩效应（Confusion）
        confusion_different_count = 0
        confusion_total_count = 0
        for _ in range(num_samples):
            plaintext = np.random.randint(0, 2, size=8)
            key = np.random.randint(0, 2, size=10)
            original_ciphertext = self.sdes.encryptOrDecrypt(plaintext, key, 'E')

            for i in range(len(key)):
                changed_key = key.copy()
                changed_key[i] = 1 - changed_key[i]
                changed_ciphertext = self.sdes.encryptOrDecrypt(plaintext, changed_key, 'E')
                different_count = np.sum(original_ciphertext!= changed_ciphertext)
                if different_count > len(original_ciphertext) / 2:
                    confusion_different_count += 1
                confusion_total_count += 1

        confusion_proportion = confusion_different_count / confusion_total_count

        return diffusion_proportion, confusion_proportion

    '''
    暴力破解
    '''
    # 单次暴力破解测试 -> 对于一个明密文对来说，可能有多个密钥与之对应
    def bruteForceAttack(self, plainText, cipherText):

        guessKeyArr = []

        cnt = 1
        start_time = time.time()
        for guessKey in range(2 ** 10):
            if np10ToDecimal(cipherText) == np10ToDecimal(self.sdes.encryptOrDecrypt(plainText, decimalToNp10(guessKey), 'E')):
                guessKeyArr.append(decimalToNp10(guessKey))
                print("暴力解出的密钥%d是:" % cnt, decimalToNp10(guessKey))   # 注意，这里的结果不止一个
                time_taken = time.time() - start_time
                cnt += 1

        return time_taken, guessKeyArr

    # 寻找碰撞
    # def foundCollision(self):



if __name__ == '__main__':
    SA = StatisticalAnalysis()
    plainText_decimal, cipherText_decimal, key_decimal = SA.generateGroup(10000) # 产生10000对数据组
    print("明文:", plainText_decimal)
    print("密文:", cipherText_decimal)
    print("密钥:", key_decimal)

    correlation = SA.correlationAnalysis('P-C', 'Pearson')
    print("明文和密文的Pearson相关系数:", correlation)
    correlation = SA.correlationAnalysis('K-C', 'Pearson')
    print("密钥和密文的Pearson相关系数:", correlation)

    rho, p_value = SA.correlationAnalysis('P-C', 'Spearman')
    print("明文和密文的Spearman统计量:", rho)
    print("明文和密文的Spearman的p值:", p_value)
    rho, p_value = SA.correlationAnalysis('K-C', 'Spearman')
    print("密钥和密文的Spearman统计量:", rho)
    print("密钥和密文的Spearman的p值:", p_value)

    # 在调用 avalancheTest 之前输出调试信息
    print("Before avalanche test")
    diffusion_proportion, confusion_proportion = SA.avalancheTest()
    print("After avalanche test")

    print("明文雪崩效应比例:", diffusion_proportion)
    print("密钥雪崩效应比例:", confusion_proportion)

    # # 绘制散点图
    # plt.scatter(plainText_decimal, cipherText_decimal, c='blue', s=3)
    # plt.xlabel('PlainText (Decimal)')
    # plt.ylabel('CipherText (Decimal)')
    # plt.title('Scatter Plot of Plaintext vs Ciphertext')
    # plt.show()


    # # 报告的散点图生成
    # # 计算明文与密文的异或为0的个数
    # xor_zero_count = np.sum(plainText_decimal == cipherText_decimal)
    #
    # # 初始化数据列表
    # output_data = []
    # # 输出key_decimal和cipherText_decimal的关系
    # for key, ct in zip(key_decimal, cipherText_decimal):
    #     # 将cipherText填充为10位二进制
    #     ct_binary = bin(ct)[2:].zfill(10)  # 将cipherText填充为10位
    #     key_binary = bin(key)[2:].zfill(10)  # 将key填充为10位
    #     # 计算二者对应位置不同元素的个数
    #     difference_count = np.sum(np.array(list(key_binary)) != np.array(list(ct_binary)))
    #     output_data.append([key, ct, difference_count])  # 将结果添加到数据列表中
    # # 打印结果
    # for row in output_data:
    #     print(f"{row},")  # 添加逗号以满足要求
    # print("明文与密文的异或为0的个数:", xor_zero_count)


    # 进行暴力破解
    plainText = np.array([1, 1, 1, 0, 0, 0, 0, 0])
    cipherText = np.array([1, 1, 1, 1, 0, 1, 1, 0])
    time_taken, _ = SA.bruteForceAttack(plainText, cipherText)
    print("用时:", time_taken)


    # 寻找碰撞













