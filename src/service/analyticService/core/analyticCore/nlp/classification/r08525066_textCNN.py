from service.analyticService.core.analyticCore.classificationBase import classification
from keras.models import Sequential
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from keras.layers import *
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from math import ceil
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class r08525066_textCNN(classification):
    def trainAlgo(self):
        self.customObj["tokenizer"]=Tokenizer(num_words=5000)
        self.customObj["tokenizer"].fit_on_texts(self.inputData['X'].reshape(-1))
        word_index=self.customObj["tokenizer"].word_index
        sequences=self.customObj["tokenizer"].texts_to_sequences(self.inputData['X'].reshape(-1))
        
        vocab_size = len(word_index) + 1
        # maxlen = 100
        # embedding_dim = 100

        x  = pad_sequences(sequences,padding='post',maxlen =self.param['max_seq_len'])

        self.model=Sequential()
        self.model.add(Embedding(vocab_size ,self.param['embed_dim'],input_length=self.param['max_seq_len'],trainable=True))
        self.model.add(Conv1D(self.param['conv_input'], 5, activation='relu'))
        self.model.add(GlobalMaxPooling1D())
        self.model.add(Dense(10, activation='relu'))
        self.model.add(Dense(self.outputData['Y'].shape[1],activation='softmax'))
        self.model.compile(optimizer=self.param['optimizer'],loss='binary_crossentropy',metrics=['accuracy'])
        self.model.fit(x, self.outputData['Y'],epochs=self.param['epochs'],verbose=False,batch_size=self.param['batch_size'])

    def predictAlgo(self):
        # self.customObj["tokenizer"]=Tokenizer()
        # self.customObj["tokenizer"].fit_on_texts(self.inputData['X'].reshape(-1))
        word_index=self.customObj["tokenizer"].word_index
        sequences=self.customObj["tokenizer"].texts_to_sequences(self.inputData['X'].reshape(-1))
        x=pad_sequences(sequences,maxlen=self.param['max_seq_len'])
        r=self.model.predict(x)
        self.result['Y']=r
