from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import *
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from math import ceil
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class r08521514_ConvRNN(classification):
    def trainAlgo(self):
        self.customObj["tokenizer"]=Tokenizer()
        self.customObj["tokenizer"].fit_on_texts(self.inputData['X'].reshape(-1))
        word_index=self.customObj["tokenizer"].word_index
        sequences=self.customObj["tokenizer"].texts_to_sequences(self.inputData['X'].reshape(-1))
        x=pad_sequences(sequences,maxlen=self.param['max_seq_len'])
        
        self.model=Sequential()
        self.model.add(Embedding(len(word_index)+1, self.param['embed_dim'], input_length=self.param['max_seq_len'], trainable=True))

        self.model.add(Convolution1D(self.param["Conv_filters"], 
                        self.param["Conv_kernalsize"], 
                        padding='same', 
                        strides = self.param["strides"], 
                        activation= self.param["Conv_activation"]))

        self.model.add(MaxPool1D(pool_size = self.param["pool_size"]))
        self.model.add(GRU(self.param["GRU_hidden1_neuron"], 
                        dropout=self.param["GRU_dropout1"], 
                        recurrent_dropout= self.param["GRU_recurrent_dropout1"], return_sequences = True))
        self.model.add(GRU(self.param["GRU_hidden2_neuron"], 
                        dropout=self.param["GRU_dropout2"], 
                        recurrent_dropout= self.param["GRU_recurrent_dropout2"]))
        self.model.add(Dense(self.outputData['Y'].shape[1], activation= self.param["Dense_activation"]))

        self.model.compile(loss='categorical_crossentropy',optimizer=self.param['optimizer'])
        self.model.fit(
            x,
            self.outputData['Y'],
            batch_size=self.param['batch_size'],
            epochs=self.param['epochs']
        )
    def predictAlgo(self):
        #self.customObj["tokenizer"]=Tokenizer()
        #self.customObj["tokenizer"].fit_on_texts(self.inputData['X'].reshape(-1))
        word_index=self.customObj["tokenizer"].word_index
        sequences=self.customObj["tokenizer"].texts_to_sequences(self.inputData['X'].reshape(-1))
        x=pad_sequences(sequences,maxlen=self.param['max_seq_len'])
        r=self.model.predict(x)
        self.result['Y']=r
