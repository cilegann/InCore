
# coding: utf-8

# In[3]:


from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPool2D 
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from service.analyticService.core.analyticCore.utils import XYdataGenerator,XdataGenerator
from math import ceil
class r07543049_num_recognitionCNN(classification):
    def trainAlgo(self):
        self.model=Sequential()
        self.model.add(Conv2D(filters = self.param['hidden_neuron'], kernel_size = (self.param['hidden_kernel_size'],self.param['hidden_kernel_size']), padding = "same", input_shape=(28,28,3), activation=self.param['hidden_activation']))
        self.model.add(MaxPool2D(pool_size=(self.param['pool_size'],self.param['pool_size'])))
        self.model.add(Conv2D(filters = self.param['hidden_neuron'], kernel_size = (self.param['hidden_kernel_size'],self.param['hidden_kernel_size']), padding = "same", input_shape=(28,28,1), activation=self.param['hidden_activation']))
        self.model.add(MaxPool2D(pool_size=(self.param['pool_size'],self.param['pool_size'])))
        self.model.add(Dropout(self.param['dropout']))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(self.param['dropout_2']))
        self.model.add(Dense(self.outputData['Y'].shape[1],activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',optimizer=self.param['optimizer'])
        self.model.fit_generator(
            XYdataGenerator(self.inputData['X'],self.outputData['Y'],28,28, self.param['batch_size']),
            steps_per_epoch=int(ceil((len(self.inputData['X'])/self.param['batch_size']))),
            epochs=self.param['epochs'], verbose = 1
        )
    def predictAlgo(self):
        
        r=self.model.predict_generator(
            XdataGenerator(self.inputData['X'],28,28,self.param['batch_size']),
            steps=int(ceil((len(self.inputData['X'])/self.param['batch_size'])))
        )
        self.result['Y']=r

