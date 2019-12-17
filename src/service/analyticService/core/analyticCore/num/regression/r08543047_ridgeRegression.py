from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import Ridge

class r08543047_ridgeRegression(regression):
    def trainAlgo(self):
        self.model=Ridge(
            alpha=self.param['alpha'],
            normalize=self.param['normalize'],
            fit_intercept=self.param['fit_intercept'],
            max_iter=self.param['max_iter'],
            tol=self.param['tol']
            )
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
