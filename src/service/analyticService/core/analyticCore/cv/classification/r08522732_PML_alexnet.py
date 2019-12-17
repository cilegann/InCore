import numpy as np
import keras
from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation,Flatten,Dropout,Dense
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from service.analyticService.core.analyticCore.utils import XYdataGenerator,XdataGenerator
from math import ceil
class r08522732_PML_alexnet(classification):
	def trainAlgo(self):
		self.model=Sequential()
		#first convolution and pooling layers
		self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),padding="valid",input_shape=(self.param['pixel'],self.param['pixel'],3),data_format='channels_last',activation=self.param['hidden_activation']))
		self.model.add(MaxPooling2D(pool_size=(3,3),strides=(2,2)))
		#second convolution and pooling layers
		self.model.add(Conv2D(256,(5,5),strides=(1,1),padding="same",activation="relu"))
		self.model.add(MaxPooling2D(pool_size=(3,3),strides=(2,2)))
		#three convolution and pooling layers
		self.model.add(Conv2D(384,(3,3),strides=(1,1),padding='same',activation='relu'))
		self.model.add(Conv2D(384,(3,3),strides=(1,1),padding='same',activation='relu'))
		self.model.add(Conv2D(256,(3,3),strides=(1,1),padding='same',activation='relu'))
		self.model.add(MaxPooling2D(pool_size=(3,3),strides=(2,2)))
		#fully connection
		self.model.add(Flatten())
		self.model.add(Dense(1024,activation='relu'))
		self.model.add(Dropout(rate=0.5))
		#classification
		self.model.add(Dense(self.outputData['Y'].shape[1],activation='softmax'))
		self.model.compile(loss='categorical_crossentropy',optimizer=self.param['optimizer'])
		self.model.fit_generator(
			XYdataGenerator(self.inputData['X'],self.outputData['Y'],self.param['pixel'],self.param['pixel'],self.param['batch_size']),
			steps_per_epoch=int(ceil((len(self.inputData['X'])/self.param['batch_size']))),
			epochs=self.param['epochs']
		)
	def predictAlgo(self):       
		r=self.model.predict_generator(
			XdataGenerator(self.inputData['X'],self.param['pixel'],self.param['pixel'],self.param['batch_size']),
			steps=int(ceil((len(self.inputData['X'])/self.param['batch_size'])))
		)
		self.result['Y']=r
