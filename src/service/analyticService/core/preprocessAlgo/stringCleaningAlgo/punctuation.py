from service.analyticService.core.preprocessAlgo.stringCleaning import stringCleaning
import string

class punctuation(stringCleaning):
    def __init__(self,data):
        super().__init__(data,"punctuation")
    def do(self):
        self.data=self.data.translate(self.data.maketrans('', '', string.punctuation))