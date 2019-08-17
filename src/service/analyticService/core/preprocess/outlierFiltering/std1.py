import numpy as np
from service.analyticService.core.preprocess.outlierFiltering import outlierFiltering

class std1(outlierFiltering):
    def __init__(self,data):
        super().__init__(data,"std1")
    def getIndex(self):
        return abs(self.data - np.mean(self.data)) < 1 * np.std(self.data)