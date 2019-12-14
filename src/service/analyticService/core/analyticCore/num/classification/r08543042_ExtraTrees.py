from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
class r08543042_ExtraTrees(classification):
    def trainAlgo(self):
        self.model=ExtraTreesClassifier(n_estimators=self.param['n_estimators'],max_features =self.param['max_features'])
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])