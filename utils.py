def sbox_index(block, axis):
    if axis == 'x':
        st = block[0]
        ed = block[-1]
    else:
        st = block[1]
        ed = block[2]
    index = f"{st}{ed}"
    return int(index, 2)
