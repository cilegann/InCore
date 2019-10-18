import matplotlib
matplotlib.use('Agg')
from service.analyticService.core.analyticCore.clusteringBase import clustering
from sklearn.cluster import KMeans
import scikitplot as skplt
import numpy as np
from sklearn.metrics import silhouette_samples,silhouette_score
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class in_kmeans(clustering):
    def trainAlgo(self):
        self.model=KMeans(n_clusters=self.param['n_clusters'],max_iter=self.param['max_iter'],algorithm=self.param['algorithm'])
        self.model.fit(self.inputData["X"])
    def predictAlgo(self):
        self.result['cluster']=self.model.predict(self.inputData["X"])
    def algoVisualize(self):
        skplt.metrics.plot_silhouette(self.inputData["X"], self.result['cluster'])
        from io import BytesIO
        import PIL
        buffer_ = BytesIO()
        plt.savefig(buffer_,format = 'png')
        buffer_.seek(0)
        dataPIL = PIL.Image.open(buffer_)
        data = np.asarray(dataPIL)
        buffer_.close()
        return {"silhouette":data}
        