from service.analyticService.core.analyticCore.abnormalBase import abnormal
from sklearn.ensemble import IsolationForest

class in_isolationForest(abnormal):
    def trainAlgo(self):
        self.model = IsolationForest(n_estimators=self.param['n_estimators'], bootstrap=self.param['bootstrap'],warm_start=self.param['warm_start'])
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result["label"]=self.model.predict(self.inputData["x"])