import numpy as np

def sbox_index(block, axis):
    # 输出目标置换盒元素的x坐标或者y坐标
    if axis == 'x':
        st = block[0]
        ed = block[-1]
    else:
        st = block[1]
        ed = block[2]
    index = f"{st}{ed}"
    return int(index, 2)

def convert_to_np_array(column):
    new_column = []
    for num in column:
        if isinstance(num, str):
            np_array = np.array(list(map(int, list(num))))
            new_column.append(np_array)
        else:
            new_column.append(num)
    return np.array(new_column)

def convert_to_decimal(binary_arr):
    result = []
    for binary_str in binary_arr:
        # 移除可能的空白字符
        binary_str = str(binary_str).strip()
        # 检查是否所有字符都是0或1
        if all(c in '01' for c in binary_str):
            # 将二进制字符串转换为十进制整数
            decimal_num = int(binary_str, 2)
            result.append(decimal_num)
        else:
            raise ValueError(f"Invalid binary number detected: {binary_str}")
    return np.array(result)


# 长度为10的二进制np数组转换为十进制
def np10ToDecimal(block):
    block = ''.join(map(str, block))
    return int(block, 2)


def decimalToNp10(decimal_value):
    # 将十进制数转换为10位二进制串，不足10位则在左边填充0
    block = f'{decimal_value:010b}'

    # 将二进制串转换为np.array，元素是0和1
    return np.array([int(bit) for bit in block])