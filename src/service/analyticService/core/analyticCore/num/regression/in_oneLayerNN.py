from service.analyticService.core.analyticCore.regressionBase import regression
from keras.models import Sequential
from keras.layers import Dense
import time
class in_oneLayerNN(regression):
    def trainAlgo(self):
        self.model=Sequential()
        self.model.add(Dense(self.param['neuron'],activation=self.param['activation'],input_dim=self.inputData['X'].shape[1],output_dim=1))
        self.model.compile(loss=self.param['loss'],optimizer=self.param['optimizer'])
        self.model.fit(self.inputData['X'],self.outputData['Y'],epochs=self.param['epochs'])
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])
