from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import HuberRegressor

class in_huberRegression(regression):
    def trainAlgo(self):
        self.model=HuberRegressor(
            epsilon=self.param['epsilon'],
            max_iter=self.param['max_iter'],
            alpha=self.param['alpha'],
            fit_intercept=self.param['fit_intercept'])
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
