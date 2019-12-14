from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import Huber

class r08525098_huberRegression(regression):
    def trainAlgo(self):
        self.model=Huber(
            alpha=self.param['alpha'],
            fit_intercept=self.param['fit_intercept'],
            max_iter=self.param['max_iter'],
            epsilon=self.param['epsilon'],
			warm_start=self.param['warm_start']
            )
        self.model.fit(self.inputData['X','CX'],self.outputData['Y'])
		
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X','CX'])
