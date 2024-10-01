import numpy as np

class SW:
    def swap(self, block):
        part1 = block[4:]
        part2 = block[:4]
        block = np.concatenate((part1, part2))
        return block