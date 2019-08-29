from service.analyticService.core.preprocessAlgo.stringCleaning import stringCleaning
import string

class punctuation(stringCleaning):
    def __init__(self,data):
        super().__init__(data,"punctuation")
    def do(self):
        for i in range(len(self.data)):
            self.data[i]=self.data[i].translate(self.data[i].maketrans('', '', string.punctuation))
        return self.data