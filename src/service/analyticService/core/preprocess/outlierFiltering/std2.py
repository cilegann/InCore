import numpy as np
from service.analyticService.core.preprocess.outlierFiltering import outlierFiltering

class std2(outlierFiltering):
    def __init__(self,data,algoName):
        super().__init__(data,algoName)
    def getIndex(self):
        return abs(self.data - np.mean(self.data)) > 2 * np.std(self.data)