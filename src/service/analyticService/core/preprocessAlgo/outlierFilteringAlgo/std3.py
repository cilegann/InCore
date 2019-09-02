import numpy as np
from service.analyticService.core.preprocessAlgo.outlierFilteringBase import outlierFiltering

class std3(outlierFiltering):
    def __init__(self,data):
        super().__init__(data,"std3")
    def getRetainIndex(self):
        return abs(self.data - np.mean(self.data)) < 3 * np.std(self.data)