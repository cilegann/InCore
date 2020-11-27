import numpy as np
from service.analyticService.core.preprocessCore.outlierFilteringBase import outlierFiltering


class negative_project(outlierFiltering):
    def __init__(self, data):
        super().__init__(data, "negative_project")

    def getRetainIndex(self):
        return self.data > 0
