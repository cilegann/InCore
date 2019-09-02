import numpy as np
from service.analyticService.core.preprocessAlgo.outlierFilteringBase import outlierFiltering

class std2(outlierFiltering):
    def __init__(self,data):
        super().__init__(data,"std2")
    def getRetainIndex(self):
        return abs(self.data - np.mean(self.data)) < 2 * np.std(self.data)