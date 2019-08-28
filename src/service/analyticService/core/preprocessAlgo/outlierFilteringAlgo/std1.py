import numpy as np
from service.analyticService.core.preprocessAlgo.outlierFiltering import outlierFiltering

class std1(outlierFiltering):
    def __init__(self,data):
        super().__init__(data,"std1")
    def getRetainIndex(self):
        return abs(self.data - np.mean(self.data)) < 1 * np.std(self.data)