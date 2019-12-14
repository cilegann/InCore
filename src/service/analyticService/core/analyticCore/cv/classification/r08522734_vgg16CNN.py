from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Flatten,MaxPooling2D, Dropout
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from service.analyticService.core.analyticCore.utils import XYdataGenerator,XdataGenerator
from math import ceil
class r08522734_vgg16CNN(classification):
    def trainAlgo(self):
        self.model=Sequential()
        
        
        a =int(self.param['hidden_neuron'])
        

        self.model.add(Conv2D((a//8),(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),input_shape=(32,32,3),data_format='channels_last',activation=self.param['hidden_activation'],padding='same'))
        self.model.add(Conv2D((a//8),(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
        self.model.add(MaxPooling2D(pool_size=(self.param['pool_size'], self.param['pool_size']),strides=(2,2)))
        
        
        
        self.model.add(Conv2D((a//4),(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
        self.model.add(Conv2D((a//4),(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
        self.model.add(MaxPooling2D(pool_size=(self.param['pool_size'], self.param['pool_size']),strides=(2,2)))

        self.model.add(Conv2D((a//2),(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
        self.model.add(Conv2D((a//2),(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
        self.model.add(Conv2D((a//2),(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
        self.model.add(MaxPooling2D(pool_size=(self.param['pool_size'], self.param['pool_size']),strides=(2,2)))
        

        if(self.param['vgg16_CCCP']):
            self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
            self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
            self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
            self.model.add(MaxPooling2D(pool_size=(self.param['pool_size'], self.param['pool_size']),strides=(2,2)))



        if(self.param['vgg16_CCCP2']):
            self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
            self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
            self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),activation=self.param['hidden_activation'],padding='same'))
            self.model.add(MaxPooling2D(pool_size=(self.param['pool_size'], self.param['pool_size']),strides=(2,2)))
       
        
        
        self.model.add(Flatten())


        if(self.param['vgg16_fc']):
            self.model.add(Dropout(self.param['dropout_value']))
            self.model.add(Dense(500,activation='softmax'))

        if(self.param['vgg16_fc2']):
            self.model.add(Dropout(self.param['dropout_value']))
            self.model.add(Dense(10,activation='softmax'))

        

        self.model.add(Dropout(self.param['dropout_value']))
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

        