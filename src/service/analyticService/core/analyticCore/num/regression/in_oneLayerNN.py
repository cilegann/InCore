from service.analyticService.core.analyticCore.regressionBase import regression
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
class in_oneLayerNN(regression):
    def trainAlgo(self):
        config = tf.ConfigProto()
        config.gpu_options.allow_growth=True
        session = tf.Session(config=config)
        KTF.set_session(session)
        self.model=Sequential()
        self.model.add(Dense(self.param['hidden_neuron'],activation=self.param['hidden_activation'],input_dim=self.inputData['X'].shape[1]))
        self.model.add(Dense(1,activation=self.param['output_activation']))
        self.model.compile(loss=self.param['loss'],optimizer=self.param['optimizer'])
        self.model.fit(self.inputData['X'],self.outputData['Y'],epochs=self.param['epochs'])
        KTF.clear_session()
    def predictAlgo(self):
        config = tf.ConfigProto()
        config.gpu_options.allow_growth=True
        session = tf.Session(config=config)
        KTF.set_session(session)
        self.result['Y']=self.model.predict(self.inputData['X'])
        KTF.clear_session()
