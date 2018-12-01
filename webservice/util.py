
import librosa
import numpy as np
import random


def random_string(l):
    def to_char(x):
        if x < 10:
            return chr(48 + x)
        if x < 36:
            return chr(55 + x)
        return chr(61 + x)
    return "".join([to_char(random.randint(0, 61)) for _ in range(l)])
