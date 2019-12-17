from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.ensemble import RandomForestClassifier
import numpy as np
class r08525098_randomForest(classification):
    def trainAlgo(self):
        self.model=RandomForestClassifier(
                                          bootstrap=self.param['bootstrap'],
                                          oob_score=self.param['oob_score'],
                                          n_estimators=self.param['n_estimators'],
                                          criterion=self.param['criterion'],
                                          max_depth=self.param['max_depth'],
                                          min_samples_split=self.param['min_samples_split'],
                                          min_samples_leaf=self.param['min_samples_leaf'],
                                          max_features=self.param['max_features'],
                                          min_weight_fraction_leaf=self.param['min_weight_fraction_leaf'],
                                          min_impurity_split=self.param['min_impurity_split'])
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict_proba(self.inputData['X'])
