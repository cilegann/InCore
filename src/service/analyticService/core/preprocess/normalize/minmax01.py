import numpy as np
from service.analyticService.core.preprocess.normalize import normalize

class minmax01(normalize):
    def __init__(self,data):
        super().__init__(data,"minmax01")
    def do(self):
        self.data=(self.data-min(self.data))/(max(self.data)-min(self.data))
        return self.data