from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Flatten,MaxPooling2D,Dropout
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from service.analyticService.core.analyticCore.utils import XYdataGenerator,XdataGenerator
from math import ceil

class r08525004_oneLayerCNN(classification):
    def trainAlgo(self):
        self.model=Sequential()
        self.model.add(Conv2D(96,(11,11),input_shape=(32,32,3),data_format='channels_last',padding='same',activation=self.param['hidden_activation']))
        self.model.add(MaxPooling2D(pool_size=(3,3),strides=(2,2)))
        
        self.model.add(Conv2D(256,(5,5),data_format='channels_last',padding='same',activation=self.param['hidden_activation']))
        self.model.add(MaxPooling2D(pool_size=(3,3),strides=(2,2)))
        
        self.model.add(Conv2D(384,(3,3),data_format='channels_last',padding='same',activation=self.param['hidden_activation']))
        self.model.add(Conv2D(384,(3,3),data_format='channels_last',padding='same',activation=self.param['hidden_activation']))
        self.model.add(Conv2D(self.param['hidden_neuron']*4,(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),data_format='channels_last',padding='same',activation=self.param['hidden_activation']))
        self.model.add(MaxPooling2D(pool_size=(3,3),strides=(2,2)))
       
        self.model.add(Flatten())
        self.model.add(Dense(4096,activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(4096,activation='relu'))
        self.model.add(Dropout(0.5))
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
