from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from keras.layers import *
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from math import ceil
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class in_oneLayerRNN(classification):
    def trainAlgo(self):
        self.customObj["tokenizer"]=Tokenizer()
        self.customObj["tokenizer"].fit_on_texts(self.inputData['X'].reshape(-1))
        word_index=self.customObj["tokenizer"].word_index
        sequences=self.customObj["tokenizer"].texts_to_sequences(self.inputData['X'].reshape(-1))
        x=pad_sequences(sequences,maxlen=self.param['max_seq_len'])
        self.model=Sequential()
        self.model.add(
            Embedding(len(word_index)+1,
            self.param['embed_dim'],
            input_length=self.param['max_seq_len'],
            trainable=True)
        )
        self.model.add(LSTM(self.param["LSTM_hidden_neuron"],activation=self.param["LSTM_hidden_activation"]))
        self.model.add(Dense(self.outputData['Y'].shape[1],activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',optimizer=self.param['optimizer'])
        self.model.fit(
            x,
            self.outputData['Y'],
            batch_size=self.param['batch_size'],
            epochs=self.param['epochs']
        )
    def predictAlgo(self):
        # self.customObj["tokenizer"]=Tokenizer()
        # self.customObj["tokenizer"].fit_on_texts(self.inputData['X'].reshape(-1))
        word_index=self.customObj["tokenizer"].word_index
        sequences=self.customObj["tokenizer"].texts_to_sequences(self.inputData['X'].reshape(-1))
        x=pad_sequences(sequences,maxlen=self.param['max_seq_len'])
        r=self.model.predict(x)
        self.result['Y']=r
