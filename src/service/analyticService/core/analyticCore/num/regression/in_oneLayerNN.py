from service.analyticService.core.analyticCore.regressionBase import regression
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
class in_oneLayerNN(regression):
    def trainAlgo(self):
        with self.session.as_default():
            with self.graph.as_default():
                self.model=Sequential()
                self.model.add(Dense(self.param['hidden_neuron'],activation=self.param['hidden_activation'],input_dim=self.inputData['X'].shape[1]))
                self.model.add(Dense(1,activation=self.param['output_activation']))
                self.model.compile(loss=self.param['loss'],optimizer=self.param['optimizer'])
                self.model.fit(self.inputData['X'],self.outputData['Y'],epochs=self.param['epochs'])
    def predictAlgo(self):
        with self.session.as_default():
            with self.graph.as_default():
                r=self.model.predict(self.inputData['X'])
                r=r.reshape(r.shape[0])
                self.result['Y']=r
