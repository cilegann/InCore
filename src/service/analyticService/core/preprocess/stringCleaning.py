class stringCleaning():
    def __init__(self,data,algoName):
        self.data=data
        self.algoName=algoName
    def do(self):
        '''
        implement in each algo (placed in strinCleaning folder)
        return a clean string based on self.data
        '''
        raise NotImplementedError(f'[stringCleaning][{self.algoName}] Not implemented error')