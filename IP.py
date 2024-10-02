import numpy as np

class IP:
    def __init__(self):
        self.ipIndex1 = np.array([2, 6, 3, 1, 4, 8, 5, 7])
        self.ipIndex2 = np.array([4, 1, 3, 5, 7, 2, 8, 6])

    # 初始置换
    def initialP(self, block):
        return block[self.ipIndex1 - 1]

    # 逆初始置换
    def initialP_Inverse(self, block):
        return block[self.ipIndex2 - 1]

