from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.tree import DecisionTreeClassifier
import numpy as np
class in_decisionTree(classification):
    def trainAlgo(self):
        self.model=DecisionTreeClassifier(
            criterion=self.param['criterion'],
            splitter=self.param['splitter'],
            min_samples_split=self.param['min_samples_split'],
            presort=self.param['presort']
            )
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
