
from service.analyticService.core.analyticCore.clusteringBase import clustering
from sklearn.cluster import AffinityPropagation



class in_affinityPropagation(clustering):
    def trainAlgo(self):
        self.model=AffinityPropagation(
            damping=self.param['damping'],
            max_iter=self.param['max_iter'],
            convergence_iter=self.param['convergence_iter'],
            # affinity=self.param['affinity']
            )
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result['cluster']=self.model.predict(self.inputData["X"])