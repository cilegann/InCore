from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
class r07945013_classification(classification):
    def trainAlgo(self):
        self.model=AdaBoostClassifier(n_estimators=self.param['n_estimators'],algorithm=self.param['algorithm'])
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
