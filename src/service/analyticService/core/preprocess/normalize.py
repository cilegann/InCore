import numpy as np

class normalize():
    def __init__(self,data,algoName):
        self.data=data
        self.algoName=algoName
    def do(self):
        '''
        implement in each algo
        return a normalized 1D numpy array based on self.data
        '''
        raise NotImplementedError(f'[Normalize][{algoName}] Not implement error')