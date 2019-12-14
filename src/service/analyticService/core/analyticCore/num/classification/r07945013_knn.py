from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
class r07945013_knn(classification):
    def trainAlgo(self):
        self.model=KNeighborsRegressor(n_neigbors=self.param['n_neigbors'],algorithm=self.param['algorithm'],p=self.param['p'])
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
