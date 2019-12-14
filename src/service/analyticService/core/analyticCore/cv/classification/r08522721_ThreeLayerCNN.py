from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Flatten,MaxPooling2D,Dropout
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from service.analyticService.core.analyticCore.utils import XYdataGenerator,XdataGenerator
from math import ceil
class r08522721_ThreeLayerCNN(classification):
	def trainAlgo(self):
		self.model=Sequential()
		a=int(self.param['hidden_neuron'])
		b=int(self.param['DropOut'])
		SZ=int(self.param['shape_size'])
		self.model.add(Conv2D(a//8,(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),input_shape=(SZ,SZ,3),data_format='channels_last',activation=self.param['hidden_activation'],padding='same'))
		self.model.add(Conv2D(a//4,(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),padding='same',activation='relu'))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Conv2D(a//2,(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),padding='same',activation='relu'))
		self.model.add(Conv2D(a,(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),padding='same',activation='relu'))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Dropout(b//2))	
		self.model.add(Conv2D(a,(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),padding='same',activation='relu'))
		self.model.add(Conv2D(a,(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),padding='same',activation='relu'))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Flatten())
		self.model.add(Dense(500,activation='relu'))
		self.model.add(Dropout(b))
		self.model.add(Dense(self.outputData['Y'].shape[1],activation='softmax'))
		
		
		
		self.model.compile(loss='categorical_crossentropy',optimizer=self.param['optimizer'])
		self.model.fit_generator(
			XYdataGenerator(self.inputData['X'],self.outputData['Y'],SZ,SZ,self.param['batch_size']),
			steps_per_epoch=int(ceil((len(self.inputData['X'])/self.param['batch_size']))),
			epochs=self.param['epochs']
		)
	def predictAlgo(self):
		SZ=int(self.param['shape_size'])
		r=self.model.predict_generator(
			XdataGenerator(self.inputData['X'],SZ,SZ,self.param['batch_size']),
			steps=int(ceil((len(self.inputData['X'])/self.param['batch_size'])))
		)
		self.result['Y']=r