from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
class ___internalTest(classification):
    def trainAlgo(self):
        self.model=KNeighborsClassifier(n_neighbors=self.param['n_neighbors'],weights=self.param['weights'],algorithm=self.param['algorithm'],p=self.param['p'])
        y=np.argmax(self.outputData['Y'],axis=1)
        x=[]
        for i in range(len(self.inputData['X'])):
            tmp=self.inputData['X'][i]
            for j in range(len(self.inputData['CX'][i])):
                tmp=np.append(tmp,self.inputData['CX'][i][j])
            x.append(tmp)
        x=np.asarray(x)
        self.model.fit(x,y)
    def predictAlgo(self):
        x=[]
        for i in range(len(self.inputData['X'])):
            tmp=self.inputData['X'][i]
            for j in range(len(self.inputData['CX'][i])):
                tmp=np.append(tmp,self.inputData['CX'][i][j])
            x.append(tmp)
        x=np.asarray(x)
        self.result['Y']=self.model.predict_proba(x)
