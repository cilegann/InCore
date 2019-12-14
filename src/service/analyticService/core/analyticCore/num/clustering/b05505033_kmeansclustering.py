
from service.analyticService.core.analyticCore.clusteringBase import clustering
from sklearn.cluster import KMeans



class b05505033_kmeansclustering(clustering):
    def trainAlgo(self):
        self.model=KMeans(
            
                n_init=self.param["n_int"],
                max_iter=self.param["max_iter"],
                tol=self.param["tollerance"],
                n_clusters=self.param["n_clusters"],
                algorithm=self.param["algorithm"],
        )
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result['cluster']=self.model.fit_predict(self.inputData["X"])