from service.analyticService.core.preprocess.stringCleaning import stringCleaning
import string

class punctuation(stringCleaning):
    def __init__(self,data,algoName):
        super().__init__(data,algoName)
    def do(self):
        for i in range(len(self.data)):
            self.data[i]=self.data[i].translate(self.data[i].maketrans('', '', string.punctuation))