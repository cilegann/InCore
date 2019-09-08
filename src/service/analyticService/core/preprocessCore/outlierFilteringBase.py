import numpy as np

class outlierFiltering():
    def __init__(self,data,algoName):
        self.data=data
        self.algoName=algoName
    def getRetainIndex(self):
        '''
        implement in each algo (placed in outlierFiltering folder)
        return a [True/False] list based on self.data
        True stands for retain (not an outlier)
        False stands for filt (an outlier)
        For Example:
        a array [1,1,1,1,1,2,50,1] filted by 1st std will return [True,True,True,True,True,True,False,True]
        '''
        raise NotImplementedError(f'[outlierFiltering][{self.algoName}] Not implement error')