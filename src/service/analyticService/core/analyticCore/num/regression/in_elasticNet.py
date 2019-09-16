from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import ElasticNet

class in_elasticNet(regression):
    def trainAlgo(self):
        self.model=ElasticNet(
            alpha=self.param['alpha'],
            l1_ratio=self.param['l1_ratio'],
            normalize=self.param['normalize'],
            fit_intercept=self.param['fit_intercept'],
            max_iter=self.param['max_iter'],
            positive=self.param['positive']
            )
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
