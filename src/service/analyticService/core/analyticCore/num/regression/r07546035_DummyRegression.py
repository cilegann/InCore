from service.analyticService.core.analyticCore.regressionBase import regression

from sklearn.dummy import DummyRegressor


class r07546035_DummyRegression(regression):
    def trainAlgo(self):
        
        self.model=DummyRegressor(
            
            strategy=self.param['strategy'],
            quantile=self.param['quantile']
            )
        
        
        self.model.fit(self.inputData['X'],self.outputData['y'],sample_weight=None)
        
        
    
    def predictAlgo(self):
        
        self.result['y']=self.model.predict(self.inputData['X'])
        
    def get_paramsAlgo(self):
        
        self.model.get_params(self)
