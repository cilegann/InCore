import numpy as np
from service.analyticService.core.preprocessCore.normalizeBase import normalize


class minmax01_project(normalize):
    def __init__(self, data):
        super().__init__(data, "minmax01_project")

    def do(self):
        self.data = 2*((self.data-min(self.data)) /
                       (max(self.data)-min(self.data))) - 1
        return self.data
