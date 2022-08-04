import numpy as np

from Singleton import SingletonMeta


class RandomNumberGenerator(metaclass=SingletonMeta):
    def __init__(self):
        self.generator: np.random.Generator = np.random.default_rng(12345)
