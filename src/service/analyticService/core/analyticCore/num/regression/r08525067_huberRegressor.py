from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn import linear_model
from sklearn.linear_model import HuberRegressor, LinearRegression
from sklearn.datasets import make_regression

class r08525067_huberRegressor(regression):
    def trainAlgo(self): #訓練
        self.model=HuberRegressor( #six parameters
            alpha=self.param['alpha'],
            fit_intercept=self.param['fit_intercept'],
            max_iter=self.param['max_iter'],
            warm_start=self.param['warm_start'],
            epsilon=self.param['epsilon'],
            tol=self.param['tol']
            )
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self): #預測
        self.result['Y']=self.model.predict(self.inputData['X'])
