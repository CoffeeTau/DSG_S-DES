import numpy as np
from utils import sbox_index

'''
f_k函数类，包含轮函数round
'''
class Function_f:
    def __init__(self):
        self.EPBox = np.array([4, 1, 2, 3, 2, 3, 4, 1])
        self.SBox1 = np.array([
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 0, 2]
        ])
        self.SBox2 = np.array([
            [0, 1, 2, 3],
            [2, 3, 1, 0],
            [3, 0, 1, 2],
            [2, 1, 0, 3]
        ])

        self.SPBox = np.array([2, 4, 3, 1])

    # 扩展(4 -> 8)
    def expandBlock(self, block):
        return block[self.EPBox - 1]

    # s盒置换 (8 -> 4)
    def sBoxSubstitution(self, block):
        left = block[:4]
        right = block[4:]

        s1_x = sbox_index(left, 'x')
        s1_y = sbox_index(left, 'y')
        s2_x = sbox_index(right, 'x')
        s2_y = sbox_index(right, 'y')

        sbox1_value = format(self.SBox1[s1_x][s1_y], '02b')
        sbox2_value = format(self.SBox2[s2_x][s2_y], '02b')

        return np.array([bit for bit in sbox1_value + sbox2_value], dtype=np.uint8) # 注意加dtype=np.uint8

    def permutationBlock(self, block):
        return block[self.SPBox - 1]

    # 轮函数
    def round(self, block, k):
        block = self.expandBlock(block)      # 扩展 (4 -> 8)
        block = block ^ k                    # 与子密钥异或 (8)
        block = self.sBoxSubstitution(block) # 替换 (8 -> 4)
        block = self.permutationBlock(block) # 置换 (4)
        return block

    # f_k函数计算
    def calculate(self, block, k):
        left = block[:4]
        right = block[4:]

        left = left ^ self.round(right, k)    # 4
        block = np.concatenate((left, right)) # 4 -> 8
        return block


if __name__ == "__main__":
    test = np.array([0, 1, 1, 1, 0, 1, 1, 0])  # 输入数据，8位
    k = np.array([1, 0, 0, 1, 0, 1, 1, 0])     # 子密钥，也应为8位
    f = Function_f()

    print("f_k函数变换结果: ", f.calculate(test, k))






