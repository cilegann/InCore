import numpy as np

class outlierFiltering():
    def __init__(self,data,algoName):
        self.data=data
        self.algoName=algoName
    def getIndex(self):
        '''
        implement in each algo
        return a [True/False] list based on self.data
        True stands for outlier
        False stands for not an outlier
        For Example:
        a array [1,1,1,1,1,2,50,1] filted by 1st std will return [False,False,False,False,False,False,True,False]
        '''
        raise NotImplementedError(f'[outlierFiltering][{algoName}] Not implement error')