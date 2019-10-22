
from service.analyticService.core.analyticCore.clusteringBase import clustering
from sklearn.cluster import AgglomerativeClustering



class in_agglomerativeClustering(clustering):
    def trainAlgo(self):
        if self.param["linkage"]=="ward":
            self.param["affinity"]="euclidean"
        if self.param["set_distance_threshold"]==1:
            self.model=AgglomerativeClustering(
                n_clusters=None,
                affinity=self.param["affinity"],
                compute_full_tree=True,
                linkage=self.param["linkage"],
                distance_threshold=self.param["distamce_threshold"]
            )
        else:
            self.model=AgglomerativeClustering(
                n_clusters=self.param["n_clusters"],
                affinity=self.param["affinity"],
                linkage=self.param["linkage"],
            )
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result['cluster']=self.model.fit_predict(self.inputData["X"])