from service.analyticService.core.analyticCore.abnormalBase import abnormal
from sklearn.svm import OneClassSVM

class in_oneClassSVM(abnormal):
    def trainAlgo(self):
        self.model = OneClassSVM(kernel=self.param['kernel'], degree=self.param['degree'],coef0=self.param['coef0'],max_iter=self.param['max_iter'])
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result["label"]=self.model.predict(self.inputData["X"])