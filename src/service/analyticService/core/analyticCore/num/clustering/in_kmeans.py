from service.analyticService.core.analyticCore.clusteringBase import clustering
from sklearn.cluster import KMeans

class in_kmeans(clustering):
    def trainAlgo(self):
        self.model=KMeans(n_clusters=self.param['n_clusters'],max_iter=self.param['max_iter'],algorithm=self.param['algorithm'])
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result['cluster']=self.model.predict(self.inputData["X"])