
from service.analyticService.core.analyticCore.clusteringBase import clustering
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler


class r08631002_DBSCANClustering(clustering):
    def trainAlgo(self):
        if self.param["auto_eps"]==0 and self.param["auto_min_samples"]==0 :
            self.model=DBSCAN(
                eps=self.param["eps"],
                min_samples=self.param["min_samples"],
                metric=self.param["metric"],
                leaf_size=self.param["leaf_size"],
                algorithm=self.param["algorithm"],
            )
        elif self.param["auto_eps"]==1 and self.param["auto_min_samples"]==1 :
            self.model=DBSCAN(
                metric=self.param["metric"],
                leaf_size=self.param["leaf_size"],
                algorithm=self.param["algorithm"],
            )
        elif self.param["auto_eps"]==1 and self.param["auto_min_samples"]==0 :
            self.model=DBSCAN(
                min_samples=self.param["min_samples"],
                metric=self.param["metric"],
                leaf_size=self.param["leaf_size"],
                algorithm=self.param["algorithm"],
            )
        elif self.param["auto_eps"]==0 and self.param["auto_min_samples"]==1 :
            self.model=DBSCAN(
                eps=self.param["eps"],
                metric=self.param["metric"],
                leaf_size=self.param["leaf_size"],
                algorithm=self.param["algorithm"],
            )
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result['cluster']=self.model.fit_predict(self.inputData["X"])