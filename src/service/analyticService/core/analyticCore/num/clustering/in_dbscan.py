
from service.analyticService.core.analyticCore.clusteringBase import clustering
from sklearn.cluster import DBSCAN



class in_dbscan(clustering):
    def trainAlgo(self):
        if self.param['auto_eps']==1 and self.param['auto_min_samples']==1:
            self.model=DBSCAN(
                eps=self.param['eps'],
                min_samples=self.param['min_samples'],
                metric=self.param['metric'],
                algorithm=self.param['algorithm'],
                leaf_size=self.param['leaf_size']  
            )
        elif self.param['auto_eps']==1:
            self.model=DBSCAN(
                eps=self.param['eps'],
                metric=self.param['metric'],
                algorithm=self.param['algorithm'],
                leaf_size=self.param['leaf_size']  
            )
        elif self.param['auto_min_samples']==1:
            self.model=DBSCAN(
                min_samples=self.param['min_samples'],
                metric=self.param['metric'],
                algorithm=self.param['algorithm'],
                leaf_size=self.param['leaf_size']  
            )
        else:
            self.model=DBSCAN(
                metric=self.param['metric'],
                algorithm=self.param['algorithm'],
                leaf_size=self.param['leaf_size']  
            )
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result['cluster']=self.model.fit_predict(self.inputData["X"])