from service.analyticService.core.analyticCore.classificationBase import classification
from sklearn.neighbors import RadiusNeighborsClassifier
import numpy as np
from keras.utils import to_categorical
class r07525032_RadiusNeighbors(classification):
    def trainAlgo(self):
        self.model=RadiusNeighborsClassifier(
		     radius=self.param['radius'],
			 weights=self.param['weights'],
			 algorithm=self.param['algorithm'],
	
			 p=self.param['p']

		
			 )
        y=np.argmax(self.outputData['Y'],axis=1)
        self.model.fit(self.inputData['X'],y)
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
        self.result['Y']=to_categorical(self.result["Y"])
