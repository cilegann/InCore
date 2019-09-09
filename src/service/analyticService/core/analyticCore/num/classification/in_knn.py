from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
class in_linearRegression(classification):
    def trainAlgo(self):
        self.model=KNeighborsClassifier(n_neighbors=self.param['n_nieghbors'],weights=self.param['weights'],algorithm=self.param['algorithm'],p=self.param['p'])
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],self.outputData['Y'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
