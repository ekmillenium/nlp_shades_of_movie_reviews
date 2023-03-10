
### Import packages ###

# Bert
from transformers import TFBertModel
import tensorflow as tf

# Spacy
import spacy
from spacy import displacy

# Basics
import pandas as pd

# Relatives
from ml_logic.data import Preprocessing



class BertModel():

    #Constructor#
    def __init__(self, backbone_model = TFBertModel, from_pretrained = "bert-base-uncased",  max_length = 256, nb_categories = 2):
        self.backbone_model = backbone_model
        self.pretrained = from_pretrained
        self.max_length = max_length
        self.nb_categories = nb_categories
        self.model = "hello"


    def build(self):
        '''
        Build a model from pretrained model and adding layers
        '''

        token_ids = tf.keras.layers.Input(shape=(self.max_length,),dtype=tf.int32,name='input_ids')
        attention_mask = tf.keras.layers.Input(shape=(self.max_length,),dtype=tf.int32,name='attention_mask')

        #load the pretrained model
        backbone = self.backbone_model.from_pretrained(self.pretrained)
        backbone.trainable = False
        x = backbone(dict(input_ids=token_ids,attention_mask=attention_mask))[1]

        #Add layers
        x = tf.keras.layers.Dense(self.max_length,activation='relu')(x)

        #define the last layer according to the number of categories in the output
        if self.nb_categories == 2:
            activation = 'sigmoid'
            output = tf.keras.layers.Dense(1,activation=activation)(x)
            print('we consider two categories')

        elif self.nb_categories == 3 or self.nb_categories == 5:
            activation = 'softmax'
            output = tf.keras.layers.Dense(self.nb_categories,activation=activation)(x)

        else:
            print('This model can only be applied to 2, 3 or 5 categories')

        #build the model
        model = tf.keras.Model(inputs=dict(input_ids=token_ids,attention_mask=attention_mask),outputs=output)


        self.model = model



    def compile(self):

        '''
        Build a compiler for the model depending on the number of classes in the target: 2, 3 or 5
        '''

        if self.nb_categories == 2:
            loss = 'binary_crossentropy'
            metrics = 'accuracy'

        elif self.nb_categories == 3 or self.nb_categories == 5:
            loss = 'sparse_categorical_crossentropy'
            metrics = [tf.keras.metrics.SparseCategoricalAccuracy('accuracy')]
        else:
            print('This model can only be applied to 2, 3 or 5 categories')

        self.model.compile(
            loss=loss,
            optimizer= 'adam',
            metrics=metrics)


    def train(self, train_tokens, val_tokens, y_train, y_val,  epochs = 3, batch_size = 64, early_stopping = 0):
        """
        fit the model on the given tokens
        """
        #Define X_train
        X_train = {
            'input_ids': train_tokens['input_ids'],
            'attention_mask': train_tokens['attention_mask']
            }
        #Define X_test
        X_val = {
            'input_ids': val_tokens['input_ids'],
            'attention_mask': val_tokens['attention_mask']
            }
        #Fit the model
        history = self.model.fit(
            x=X_train,
            y=y_train,
            validation_data = (X_val, y_val),
            epochs=epochs,
            batch_size=batch_size
            )

        return history



    def predict(self, tokens):
        '''
        returns the prediction for given reviews, the input should have been tokenized before using an adapted tokenizer
        '''
        X = {
            'input_ids': tokens['input_ids'],
            'attention_mask': tokens['attention_mask']
            }
        return self.model.predict(X)



class NerModel():

    # Constructor #
    def __init__(self, pretrained_model: str = None, review: str = None):
        self.pretrained_model = pretrained_model
        self.review = review


    def load(self):
        model = spacy.load(self.pretrained_model)
        return model


    def extract_content(self, model):
        doc = model(self.review)
        sentences_extracted = []

        if doc.ents != ():
            for ent in  doc.ents:
                if ent.label_ == "PERSON":
                    if ent.sent not in sentences_extracted:
                        sentences_extracted.append(ent.sent)

        return ' '.join(str(sent) for sent in sentences_extracted)


    def extract_people(self, model):
        doc = model(self.review)
        people_extracted= []

        if doc.ents != ():
            for ent in  doc.ents:
                if ent.label_ == "PERSON":
                    if ent.text not in people_extracted:
                        people_extracted.append(ent.text)

        return ' '.join(str(sent) for sent in people_extracted)
