from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

class r06546050_Polynomial_regression(regression):

    def trainAlgo(self):
        self.premodel = PolynomialFeatures(degree = self.param['degree'],
            interaction_only = self.param['interaction_only'],
            include_bias = self.param['include_bias'],
            order = self.param['order']
            )
        self.after_trans = self.premodel.fit_transform(self.inputData['X'])
        self.model = LinearRegression(fit_intercept = self.param['fit_intercept'],
            normalize = self.param['normalize'],
            copy_X = self.param['copy_X']
            )
        self.model.fit(self.after_trans,self.outputData['Y'])
        self.customObj['record_for_poly']=np.array([self.param['degree'],self.param['interaction_only'],self.param['include_bias'],self.param['order']])

    def predictAlgo(self):
        BB=self.customObj['record_for_poly']
        self.premodel = PolynomialFeatures(degree = int(BB[0]),
            interaction_only = int(BB[1]),
            include_bias = int(BB[2]),
            order = BB[3]
            )
        self.pafter_trans = self.premodel.fit_transform(self.inputData['X'])
        self.result['Y']=self.model.predict(self.pafter_trans)
