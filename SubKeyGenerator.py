import numpy as np

class SubKeyGenerator:
    def __init__(self):
        self.PBox10 = np.array([3, 5, 2, 7, 4, 10, 1, 9, 8, 6])
        self.PBox8 = np.array([6, 3, 7, 4, 8, 5, 10, 9])

    def permutation10(self, block):
        return block[self.PBox10 - 1]

    def permutation8(self, block):
        return block[self.PBox8 - 1]

    def subKeyGenerateShift1(self, block):
        parts = [block[1:5], block[[0]], block[6:], block[[5]]]
        block = np.concatenate(parts)
        return block

    def subKeyGenerateShift2(self, block):
        parts = [block[2:5], block[0:2], block[7:], block[5:7]]
        block = np.concatenate(parts)
        return block

    def generate(self, initialKey, k):
        """密钥生成函数 k为1 则生成子密钥1 k为2 则生成子密钥2 """
        if len(initialKey) != 10:
            print("您输入的密钥位数应为10位！")
            return 0

        temp1 = self.permutation10(initialKey)
        if len(temp1) != 10:
            print("P10错误！")
        print("P10之后为：", temp1)

        if k == 1:
            temp2 = self.subKeyGenerateShift1(temp1)
        elif k == 2:
            temp2 = self.subKeyGenerateShift2(temp1)
        print("shift之后为：", temp2)
        if (len(temp2) != 10):
            print("shift错误!")
            return

        key = self.permutation8(temp2)
        if (len(key) != 8):
            print("子密钥生成错误！")
            return

        print("子密钥为", key)
        return key


if __name__ == '__main__':
    initialKey = np.array([1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
    subkeygenerator = SubKeyGenerator()
    subkeygenerator.generate(initialKey, 1)


