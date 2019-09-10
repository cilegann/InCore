from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import LinearRegression
import time
class in_stopTest(regression):
    def trainAlgo(self):
        self.model=LinearRegression()
        self.model.fit(self.inputData['X'],self.outputData['Y'])
        time.sleep(600)
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
