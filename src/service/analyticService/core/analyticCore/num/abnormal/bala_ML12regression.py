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
        input_length, input_dim = self.inputData['X'].shape[1],self.inputData['X'].shape[2]

        inputs = Input(shape=(input_length, input_dim,)) 

        lstm_out =Bidirectional(LSTM(20,return_sequences=True))(inputs)
        lstm_out =PReLU()(lstm_out)
        decode = TimeDistributed(Dense(input_dim, activation='elu'))(lstm_out)
        self.model = Model(inputs=[inputs], outputs=decode)
        self.model.compile(loss='MSE',optimizer=tf.keras.optimizers.Adam(lr=0.001))
        callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto", restore_best_weights=True)
        self.model.fit(self.inputData['X'],self.inputData['X'],batch_size=16,verbose=0,epochs=10,validation_split=0.1,callbacks=[callback])

        self.param['n_estimators']
        # self.model=Sequential()
        # self.model.add(Dense(16,activation='linear',input_dim=self.inputData['X'].shape[1]))
        # self.model.add(Dense(1,activation='linear'))
        # self.model.add(Bidirectional(LSTM()))
        # self.model.compile(loss='mean_squared_error',optimizer='sgd')
        # self.model.fit(self.inputData['X'],self.outputData['Y'],epochs=20)
    def predictAlgo(self):
        self.result['Y']=self.model.predict(self.inputData['X'])