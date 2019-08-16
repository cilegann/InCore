import numpy as np

class normalize():
    def __init__(self,data,algoName):
        self.data=data
        self.algoName=algoName
    def do(self):
        raise NotImplementedError(f'[Normalize][{algoName}] Not implement error')