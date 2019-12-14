from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import TheilSenRegressor


class r07522507_TheilSenRegressor(regression):
    def trainAlgo(self):
        self.model=TheilSenRegressor(
            fit_intercept=self.param['fit_intercept'],
            copy_X=self.param['copy_X'],
            max_subpopulation=self.param['max_subpopulation'],
            n_subsamples=self.param['n_subsamples'],
            max_iter=self.param['max_iter'],
            tol=self.param['tol'],
            random_state=self.param['random_state'],
            verbose=self.param['verbose'],
            )
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
