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

    # 字符串填充
    def padString(self, s):
        # 计算需要填充的字节数
        padding_length = 8 - (len(s) % 8)
        if padding_length == 0:
            padding_length = 8
        padding_char = chr(padding_length).encode('utf - 8')
        return s.encode('utf - 8') + padding_char * padding_length

    def unpadString(self, s):
        padding_length = s[-1]
        return s[: - padding_length].decode('utf - 8')

    # type == 'E' : 该过程为加密过程
    # type == 'D' : 该过程为解密过程
    def encryptOrDecrypt(self, text, key, type):
        # 生成子密钥k1和k2
        k1 = self.subkeygenerator.generate(key, 1)
        k2 = self.subkeygenerator.generate(key, 2)

        # 初始置换IP
        text = self.ip.initialP(text)

        # 第一次轮函数计算(加密和解密只有f_{k1}和f_{k2}的使用顺序不同)
        if type == 'E':
            text = self.function_f.calculate(text, k1)
        elif type == 'D':
            text = self.function_f.calculate(text, k2)

        # SW
        text = self.sw.swap(text)

        # 第二次轮函数计算(加密和解密只有f_{k1}和f_{k2}的使用顺序不同)
        if type == 'E':
            text = self.function_f.calculate(text, k2)
        elif type == 'D':
            text = self.function_f.calculate(text, k1)

        # 逆初始置换IP^{-1}
        text = self.ip.initialP_Inverse(text)  # 初始置换

        # if type == 'E':
        #     print("加密结果为:", text)
        # else:
        #     print("解密结果为:", text)

        return text

    def encryptString(self, s, key):
        padded_s = self.padString(s)
        encrypted_array = []
        for i in range(0, len(padded_s), 8):
            block = np.array(list(padded_s[i:i + 8]))
            encrypted_block = self.encryptOrDecrypt(block, key, 'E')
            encrypted_array.extend(encrypted_block)
        return bytes(encrypted_array).hex()

    def decryptString(self, s_hex, key):
        s = bytes.fromhex(s_hex)
        decrypted_array = []
        for i in range(0, len(s), 8):
            block = np.array(list(s[i:i + 8]))
            decrypted_block = self.encryptOrDecrypt(block, key, 'D')
            decrypted_array.extend(decrypted_block)
        return self.unpadString(bytes(decrypted_array))

    def encryptString(self, s, key):
        binary_s = ''.join(format(ord(c), 'b').zfill(8) for c in s)
        encrypted_binary = ''
        for i in range(0, len(binary_s), 8):
            block = np.array(list(map(int, list(binary_s[i:i + 8]))), dtype=np.uint8)
            encrypted_block = self.encryptOrDecrypt(block, key, 'E')
            encrypted_binary += ''.join(str(b) for b in encrypted_block)
        encrypted_chars = []
        for i in range(0, len(encrypted_binary), 8):
            num = int(encrypted_binary[i:i + 8], 2)
            encrypted_chars.append(chr(num))
        return ''.join(encrypted_chars)

    def decryptString(self, s, key):
        binary_s = ''.join(format(ord(c), 'b').zfill(8) for c in s)
        decrypted_binary = ''
        for i in range(0, len(binary_s), 8):
            block = np.array(list(map(int, list(binary_s[i:i + 8]))), dtype=np.uint8)
            decrypted_block = self.encryptOrDecrypt(block, key, 'D')
            decrypted_binary += ''.join(str(b) for b in decrypted_block)
        decrypted_chars = []
        for i in range(0, len(decrypted_binary), 8):
            num = int(decrypted_binary[i:i + 8], 2)
            decrypted_chars.append(chr(num))
        return ''.join(decrypted_chars)

if __name__ == "__main__":
    p = np.array([1, 1, 1, 0, 0, 0, 0, 0])
    key = np.array([0,1,0,0,0,0,0,0,0,0])
    # c = np.array([1,1,1,0,1,0,1,1])
    sdes = SDES()
    p = sdes.encryptOrDecrypt(p, key, 'E')
    print("bit密文:", p)

    # p_str = "Default Security Group"
    # encrypted_result = sdes.encryptString(p_str, key)
    # print("字符串密文:", encrypted_result)
    # decrypted_result = sdes.decryptString(encrypted_result, key)
    # print("字符串明文:", decrypted_result)