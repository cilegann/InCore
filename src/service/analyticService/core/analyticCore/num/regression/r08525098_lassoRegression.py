from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import BayesianRidge
from keras.models import Sequential
from keras.layers import Dense,Dropout

class r08525098_lassoRegression(regression):
    def trainAlgo(self):
        self.model=BayesianRidge(
            n_iter=self.param['n_iter'],
            tol=self.param['tol'],
            alpha_1=self.param['alpha_1'],
            alpha_2=self.param['alpha_2'],
            lambda_1=self.param['lambda_1'],
            lambda_2=self.param['lambda_2'],
            lambda_init=self.param['lambda_init'],
            compute_score=self.param['compute_score'],
            fit_intercept=self.param['fit_intercept'],
            normalize=self.param['normalize'],
            copy_X=self.param['copy_X'],
            verbose=self.param['verbose']
            )
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
