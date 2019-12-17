from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import Lasso

class d08525001_huberRegression(regression):
    def trainAlgo(self):
        self.model=Lasso(
            alpha=self.param['alpha'],
            normalize=self.param['normalize'],
            fit_intercept=self.param['fit_intercept'],
            max_iter=self.param['max_iter'],
            positive=self.param['positive']
            )
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
