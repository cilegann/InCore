from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import LinearRegression

class in_linearRegression(regression):
    def trainAlgo(self):
        self.model=LinearRegression(fit_intercept=self.param['fit_intercept'],normalize=self.param['normalize'])
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
