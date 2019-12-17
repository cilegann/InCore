from service.analyticService.core.analyticCore.classificationBase import classification
from service.analyticService.core.analyticCore.utils import XYdataGenerator,XdataGenerator
from math import ceil
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from keras.models import Sequential
from keras.layers import  Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D

class r07525116_algo(classification):
    def trainAlgo(self):

        # 建立Keras 的 Sequential 模型
        self.model = Sequential()

        # 建立捲積層 1
        self.model.add(
            Conv2D(self.param['hidden_neuron'],
                  (self.param['hidden_kernel_size'],self.param['hidden_kernel_size'] ),
                  input_shape=(32,32,3),
                  activation=self.param['hidden_activation'],
                  padding='same'))


        # 加入Dropout 避免 overfitting
        self.model.add(Dropout( self.param['dropout'] ))

        # 建立池化層 1
        self.model.add(MaxPooling2D(pool_size=(2,2)))

        # 建立捲積層 2
        self.model.add(Conv2D(filters=64,kernel_size=(3,3),activation='relu',padding='same'))
        # 加入Dropout 避免 overfitting
        self.model.add(Dropout( self.param['dropout'] ))
        
        # 建立池化層 2
        self.model.add(MaxPooling2D(pool_size=(2,2)))

        # 建立平坦層
        self.model.add(Flatten())
        # 加入Dropout 避免 overfitting
        self.model.add(Dropout(self.param['dropout']))

        # 建立隱藏層
        self.model.add(Dense(1024,activation='relu'))
        self.model.add(Dropout(self.param['dropout']))

        # 建立輸出層
        self.model.add(Dense(self.outputData['Y'].shape[1],activation='softmax'))
        #定義訓練方式
        self.model.compile(loss='categorical_crossentropy',optimizer=self.param['optimizer'])
        #開始訓練
        self.model.fit_generator(
            XYdataGenerator(self.inputData['X'],self.outputData['Y'],32,32,self.param['batch_size']),
            steps_per_epoch=int(ceil((len(self.inputData['X'])/self.param['batch_size']))),
            epochs=self.param['epochs'])
    def predictAlgo(self):        
        r=self.model.predict_generator(XdataGenerator(self.inputData['X'],32,32,self.param['batch_size']),steps=int(ceil((len(self.inputData['X'])/self.param['batch_size']))))
        self.result['Y']=r