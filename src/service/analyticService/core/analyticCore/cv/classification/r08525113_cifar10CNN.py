from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D,Dropout,Activation,GlobalMaxPooling2D
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from service.analyticService.core.analyticCore.utils import XYdataGenerator, XdataGenerator
from math import ceil


class r08525113_cifar10CNN(classification):
    def trainAlgo(self):
        self.model = Sequential()
        self.model.add(Conv2D(self.param['hidden_neuron'],(self.param['hidden_kernel_size'],self.param['hidden_kernel_size']),input_shape=(32,32,3),activation=self.param['hidden_activation'],padding = 'same'))

        self.model.add(Conv2D(32, (3, 3),input_shape=(32,32,3),padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(32, (3, 3),input_shape=(32,32,3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(48, (3, 3),input_shape=(32,32,3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(48, (3, 3), input_shape=(32, 32, 3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(self.param['dropout']))

        self.model.add(Conv2D(80, (3, 3),input_shape=(32,32,3),padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(80, (3, 3),input_shape=(32,32,3),padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(80, (3, 3),input_shape=(32,32,3),padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(80, (3, 3),input_shape=(32,32,3),padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(80, (3, 3),input_shape=(32,32,3),padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(self.param['dropout']))

        self.model.add(Conv2D(128, (3, 3), input_shape=(32, 32, 3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(128, (3, 3), input_shape=(32, 32, 3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(128, (3, 3), input_shape=(32, 32, 3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(128, (3, 3), input_shape=(32, 32, 3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(Conv2D(128, (3, 3), input_shape=(32, 32, 3), padding='same'))
        self.model.add(Activation(self.param['hidden_activation']))

        self.model.add(GlobalMaxPooling2D())
        self.model.add(Dropout(self.param['dropout']))

        self.model.add(Dense(500, activation='relu'))
        self.model.add(Dropout(self.param['dropout2']))
        self.model.add(Dense(self.outputData['Y'].shape[1], activation='softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer=self.param['optimizer'],metrics=['accuracy'])
        self.model.fit_generator(
            XYdataGenerator(self.inputData['X'], self.outputData['Y'], 32, 32, self.param['batch_size']),
            steps_per_epoch=int(ceil((len(self.inputData['X'])/self.param['batch_size']))),
            epochs=self.param['epochs']
        )

    def predictAlgo(self):
        r = self.model.predict_generator(
            XdataGenerator(self.inputData['X'], 32, 32, self.param['batch_size']),
            steps=int(ceil((len(self.inputData['X']) / self.param['batch_size'])))
        )
        self.result['Y'] = r
