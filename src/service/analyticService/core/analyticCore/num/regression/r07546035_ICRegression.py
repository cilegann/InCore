from service.analyticService.core.analyticCore.regressionBase import regression

from sklearn.linear_model import LassoLarsIC


class r07546035_ICRegression(regression):
    def trainAlgo(self):
        
        self.model=LassoLarsIC(
            
            criterion=self.param['criterion'],
            fit_intercept=self.param['fit_intercept'],
            normalize=self.param['normalize'],
            max_iter=self.param['max_iter'],
            eps=self.param['eps'],
            positive=self.param['positive']
           
            )
        self.model.score(self.inputData['X'],self.outputData['Y'])
        self.model.fit(self.inputData['X'],self.outputData['Y'])
        self.model.get_params(self)
        
    
    
    def predictAlgo(self):
        
        self.result['Y']=self.model.predict(self.inputData['X'])
