from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.svm import LinearSVC
import numpy as np
class in_linearSVC(classification):
    def trainAlgo(self):
        self.model=LinearSVC(
            penalty=self.param['penalty'],
            loss=self.param['loss'],
            dual=self.param['dual'],
            multi_class=self.param['multi_class'],
            fit_intercept=self.param['fit_intercept']
            )
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
