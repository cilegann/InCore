from service.analyticService.core.analyticCore.abnormalBase import abnormal
from sklearn.neighbors import LocalOutlierFactor

class in_localOutlierFactor(abnormal):
    def trainAlgo(self):
        if self.param['metric']=='minkowski':
            self.model = LocalOutlierFactor(
                    n_neighbors=self.param["n_neighbors"],
                    algorithm=self.param["algorithm"],
                    leaf_size=self.param["leaf_size"],
                    metric='minkowski',
                    p=self.param['p'],
                    novelty=True
            )
        else:
            self.model = LocalOutlierFactor(
                    n_neighbors=self.param["n_neighbors"],
                    algorithm=self.param["algorithm"],
                    leaf_size=self.param["leaf_size"],
                    metric=self.param['metric'],
                    novelty=True
            )
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result["label"]=self.model.predict(self.inputData["X"])