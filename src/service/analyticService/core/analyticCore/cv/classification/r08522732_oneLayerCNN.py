from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Flatten
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from service.analyticService.core.analyticCore.utils import XYdataGenerator,XdataGenerator
from math import ceil
class r08522732_oneLayerCNN(classification):
    def trainAlgo(self):
        self.model=Sequential()
        self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),input_shape=(32,32,3),data_format='channels_last',activation=self.param['hidden_activation']))
        self.model.add(Flatten())
        self.model.add(Dense(self.outputData['Y'].shape[1],activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',optimizer=self.param['optimizer'])
        self.model.fit_generator(
            XYdataGenerator(self.inputData['X'],self.outputData['Y'],32,32,self.param['batch_size']),
            steps_per_epoch=int(ceil((len(self.inputData['X'])/self.param['batch_size']))),
            epochs=self.param['epochs']
        )
    def predictAlgo(self):
        
        r=self.model.predict_generator(
            XdataGenerator(self.inputData['X'],32,32,self.param['batch_size']),
            steps=int(ceil((len(self.inputData['X'])/self.param['batch_size'])))
        )
        self.result['Y']=r
