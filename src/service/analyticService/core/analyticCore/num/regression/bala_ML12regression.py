from service.analyticService.core.analyticCore.regressionBase import regression

import tensorflow as tf
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Dense,multiply,Input,LSTM,Flatten,Activation,Dropout,RepeatVector,Reshape,Lambda,Permute
from tensorflow.keras.layers import TimeDistributed,Bidirectional,Convolution1D,MaxPooling1D,UpSampling1D,concatenate
from tensorflow.keras.regularizers import l1
import tensorflow.keras.backend as K 
from tensorflow.keras.layers import LeakyReLU,PReLU
from sklearn.metrics import mean_squared_error #均方误差
from sklearn.metrics import mean_absolute_error #平方绝对误差
from sklearn.metrics import r2_score#R square
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import metrics

class bala_ML12regression(regression):
    def trainAlgo(self):
        # self.model = Sequential()
        # self.model.add(Bidirectional(LSTM(20, return_sequences=True), input_shape=(self.inputData['X'].shape[0], self.inputData['X'].shape[1])))
        # self.model.add(PReLU())
        # self.model.add(TimeDistributed(Dense(self.inputData['X'].shape[1]), activation='elu'))
        # self.model.compile(loss='MSE',optimizer=tf.keras.optimizers.Adam(lr=0.001))
        # callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto", restore_best_weights=True)
        # self.model.fit(self.inputData['X'],self.outputData['Y'],batch_size=16,verbose=0,epochs=self.param['epochs'],validation_split=0.1,callbacks=[callback])



        input_length, input_dim = self.inputData['X'].shape[0],self.inputData['X'].shape[1]

        inputs = Input(shape=(input_length, input_dim, )) 

        lstm_out = Bidirectional(LSTM(20,return_sequences=True))(inputs)
        lstm_out = PReLU()(lstm_out)
        decode = TimeDistributed(Dense(input_dim, activation='relu'))(lstm_out)
        self.model = Model(inputs=[inputs], outputs=decode)
        self.model.compile(loss='MSE',optimizer=tf.keras.optimizers.Adam(lr=0.001))
        callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto", restore_best_weights=True)
        self.model.fit(self.inputData['X'],self.outputData['Y'],batch_size=16,verbose=0,epochs=self.param['epochs'],validation_split=0.1,callbacks=[callback])

    def predictAlgo(self):
        r=self.model.predict(self.inputData['X'])
        r=r.reshape(r.shape[0])
        self.result['Y']=r