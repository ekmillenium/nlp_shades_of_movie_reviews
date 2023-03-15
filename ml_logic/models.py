
'''
Import packages
'''

# BERT and BART
from transformers import TFBertModel, AutoTokenizer, BartForConditionalGeneration
import tensorflow as tf

# Spacy
import spacy
from spacy import displacy

# Basics
import pandas as pd

# Relatives
from ml_logic.data import Preprocessing


class BertModel():

    def __init__(self, backbone_model = TFBertModel, from_pretrained = "bert-base-uncased",  max_length = 512, nb_categories = 3):
        self.backbone_model = backbone_model
        self.pretrained = from_pretrained
        self.max_length = max_length
        self.nb_categories = nb_categories
        self.model = None


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
        x = tf.keras.layers.Dense(128,activation='relu')(x)
        x = tf.keras.layers.Dense(32,activation='relu')(x)

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


    def load(self):
        '''
        Load an existing model located in a given path
        '''

        self.model = TFBertModel.from_pretrained("bert-base-uncased")





class NerModel():

    def __init__(self, pretrained_model: str = None, review: str = None):
        self.pretrained_model = pretrained_model
        self.review = review


    def load(self):
        model = spacy.load(self.pretrained_model)
        return model


    def extract_content(self, model):
        doc = model(self.review)
        sentences_extracted = []
        sentences_extracted_labelized = []

        if doc.ents != ():
            for ent in  doc.ents:
                if ent.label_ == "PERSON":
                    if ent.sent not in sentences_extracted:
                        sentences_extracted.append(ent.sent)
                        sentences_extracted_labelized.append(displacy.render(model(str(ent.sent)), style="ent", options={'ents': ['PERSON']}))

        return ' '.join(str(sent) for sent in sentences_extracted), ' '.join(str(sent) for sent in sentences_extracted_labelized)


    def extract_people(self, model):
        doc = model(self.review)
        people_extracted= []

        if doc.ents != ():
            for ent in  doc.ents:
                if ent.label_ == "PERSON":
                    if ent.text not in people_extracted:
                        people_extracted.append(ent.text)

        return ' '.join(str(sent) for sent in people_extracted)

class BartModel():

    #Constructor#
    def __init__(self, tokenizer = AutoTokenizer, backbone_model = BartForConditionalGeneration, from_pretrained = "facebook/bart-large-cnn",  min_length = 0, max_length = 100):
        self.tokenizer = tokenizer.from_pretrained(from_pretrained)
        self.backbone_model = backbone_model
        self.from_pretrained = from_pretrained
        self.min_length = min_length
        self.max_length = max_length

    def tokenize(self, sentences):
        '''
        Tokenize data depending on the type of tokenizer used.
        Output is a list that includes the sequence of tokens and its length.
        '''
        token_sequence = self.tokenizer(sentences, max_length=1024, truncation=True, return_tensors="pt")['input_ids'] # Sequence of tokens

        token_count = len(token_sequence[0]) # Count number of tokens in sequence
        return [token_sequence, token_count]

    def get_summary_from_sequence(self, sequence):
        '''
        Generate summary from sequence of tokens depending on the chosen backbone model.
        Output is a string.
        '''
        model = self.backbone_model.from_pretrained(self.from_pretrained)
        summary_ids = model.generate(sequence, num_beams=2, min_length=self.min_length, max_length=self.max_length)
        return self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    def get_summary_from_text(self, full_text):
        '''
        Generate summary from string depending on the chosen backbone model.
        Output is a string.
        '''
        sequence = self.tokenize(full_text)[0]
        return self.get_summary_from_sequence(sequence)

    # Extract scraped reviews for a movie from the dataset
    """ Warning: This needs to be reworked once the get data function is built. """
    def get_reviews_for_movie(self, tconst, review_count):
        df = pd.read_csv("../raw_data/reviews_vf.csv")
        reviews_for_a_movie = df[df["tconst"] == tconst].copy()
        total_reviews = reviews_for_a_movie.shape[0]
        if total_reviews < review_count:
            review_count = total_reviews
        reviews_for_a_movie = reviews_for_a_movie.iloc[0:review_count]
        #reviews_for_a_movie["content"] = reviews_for_a_movie["content"].apply(basic_preprocessing)

        return reviews_for_a_movie

    # Summarize scraped reviews
    """ Warning: This needs to be reworked once the get data function is built. """
    def review_summarizer(self, df, column="content"):
        ''' Input is a Panda series, output is list of summaries. '''
        df["summary"] = df["content"].apply(lambda x: self.get_summary_from_text(x))
        summaries = df["summary"].tolist()
        return summaries

    def get_chunks(self, summaries):
        '''
        Function to create chunk of summaries from a list of summaries.
        Output is a dictionary of chunks.
        '''
        master_dict = {}
        token_counter = 0
        key_counter = 0

        for i in range(len(summaries)):

            full_text = summaries[i]
            tokens = self.tokenize(full_text)[1] # Sequence length
            token_counter += tokens

            if token_counter < 1024:
                if i == 0:
                    master_dict[key_counter] = summaries[i]
                else:
                    master_dict[key_counter] = master_dict[key_counter] + " " + summaries[i]

            else:
                token_counter = tokens
                key_counter += 1
                master_dict[key_counter] = summaries[i]

        return master_dict

    def chunk_summarizer(self, chunks_dict):
        '''
        Summarize chunks and generate a list of summaries.
        Used in function iterative_summarizer
        '''
        summaries_list = []
        for key in chunks_dict:
            summary = self.get_summary_from_text(chunks_dict[key])
            summaries_list.append(summary)
        return summaries_list

    def iterative_summarizer(self, chunks_dict):
        '''
        Summarize summaries until there is one chunck left
        '''
        print(f'''{len(chunks_dict)} chunk(s) will be summarized.''') # DELETE

        # Summarize each chunk and concatenate all the summaries in a list of summaries
        summaries_list = self.chunk_summarizer(chunks_dict)

        # Generate chunks from new list of summaries
        chunks_dict = self.get_chunks(summaries_list)
        print(f'''{len(chunks_dict)} new chunk(s) was/were created.''') # DELETE
        if len(chunks_dict) > 1:
            self.iterative_summarizer(chunks_dict)
        return self.get_summary_from_text(chunks_dict[0])

    def get_summary_for_movie(self, tconst, review_count):
        '''
        Master function to get summary for a given movie based on unique identifier and predefined number of reviews
        '''
        reviews_for_a_movie = self.get_reviews_for_movie(tconst, review_count)
        print(f"""{reviews_for_a_movie.shape[0]} reviews will be summarized.""") #DELETE
        summaries = self.review_summarizer(reviews_for_a_movie, "content")
        print(f"""{len(summaries)} reviews were summarized.""") #DELETE
        chunks_dict = self.get_chunks(summaries)
        summary = self.iterative_summarizer(chunks_dict)
        return summary

    def get_summary_demo_day(self, df, review_limit):
        '''
        Master function to get summary for a given movie during the demo day.
        Df is the dataframe returned by the parser.
        Review_limit is the number of reviews to summarize.
        '''
        total_reviews = df.shape[0]
        if total_reviews < review_limit:
            review_limit = total_reviews
        df = df.iloc[0:review_limit]
        summaries = self.review_summarizer(df, "content")
        print(f"""{len(summaries)} reviews were summarized.""") #DELETE
        chunks_dict = self.get_chunks(summaries)
        summary = self.iterative_summarizer(chunks_dict)
        return summary
