from service.analyticService.core.analyticCore.abnormalBase import abnormal
from sklearn.covariance import EllipticEnvelope

class in_ellipticEnvelope(abnormal):
    def trainAlgo(self):
        if self.param['set_support_fraction']==0:
            support_fraction=None
        else:
            support_fraction=self.param['support_fraction']
        self.model=EllipticEnvelope(
            assume_centered=self.param['assume_centered'],
            support_fraction=support_fraction,
            contamination=self.param['contamination']
        )    
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result["label"]=self.model.predict(self.inputData["X"])
        # self.txtRes+=f"score_samples: {self.model.score_samples(self.inputData['X'])}\n"