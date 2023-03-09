
from transformers import TFBertModel
import tensorflow as tf



class BertModel():

    #Constructor#
    def __init__(self, backbone_model = TFBertModel, from_pretrained = "bert-base-uncased",  max_length = 256, nb_categories = 2):
        self.backbone_model = backbone_model
        self.pretrained = from_pretrained
        self.max_length = max_length
        self.nb_categories = nb_categories


    def build_model(self):
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
        x = tf.keras.layers.Dense(128,activation='relu')(x)

        #define the last layer according to the number of categories in the output
        if self.nb_categories == 2:
            activation = 'sigmoid'
        elif self.nb_categories == 3 or self.nb_categories == 5:
            activation = 'softmax'

        else:
            print('This model can only be applied to 2, 3 or 5 categories')

        output = tf.keras.layers.Dense(self.nb_categories,activation=activation)(x)

        #build the model
        model = tf.keras.Model(inputs=dict(input_ids=token_ids,attention_mask=attention_mask),outputs=output)

        return model


    def compile_model(self):

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


    def train_model(self, tokens, y, epochs = 3, batch_size = 256):
        history = self.model.fit(
            x={'input_ids':tokens['input_ids'], 'attention_mask':tokens['attention_mask']},
            y=y,
            epochs=epochs,
            batch_size=batch_size
            )

        return history



    def predict(self):
        pass
