from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
class ___internalTest(classification):
    def trainAlgo(self):
        self.model=KNeighborsClassifier(n_neighbors=self.param['n_neighbors'],weights=self.param['weights'],algorithm=self.param['algorithm'],p=self.param['p'])
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
