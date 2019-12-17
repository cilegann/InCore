from service.analyticService.core.analyticCore.regressionBase import regression
from sklearn.linear_model import Lasso

class d08525001_priceRegression(regression):
    def trainAlgo(self):
        self.model=Lasso(
            price=self.param['price'],
            guest_rating=self.param['guest_rating'],
            star_rate=self.param['star_rate'],
            check_in_date=self.param['check_in_date'],
            )
        self.model.fit(self.inputData['X','CX'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X','CX'])
