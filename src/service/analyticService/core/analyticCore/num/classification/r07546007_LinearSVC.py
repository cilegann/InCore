from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import numpy as np


class r07546007_LinearSVC(classification):
    def trainAlgo(self):
        self.model= LinearSVC(
            C=self.param['C'],
            penalty=self.param['penalty'],
            dual=self.param['dual'],
            max_iter=self.param['max_iter']
            
            )
        self.model=CalibratedClassifierCV(self.model) 
        y=np.argmax(self.outputData['Y'],axis=1)


        self.model.fit(self.inputData['X'],y)


    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
