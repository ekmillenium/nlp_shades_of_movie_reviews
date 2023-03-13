
'''
Import packages
'''

# Bert
from transformers import BertTokenizer
#import tensorflow as tf


class Tokenizer():

    def __init__(self, tokenizer = BertTokenizer, from_pretrained = "bert-base-uncased", max_length = 512):
        self.tokenizer = tokenizer.from_pretrained(from_pretrained)
        self.max_length = max_length


    def tokenize_bert(self, sentences):
        '''
        function used to tokenize data depending on the type of tokenizer used
        '''
        tokens = self.tokenizer(list(sentences),
                         max_length = self.max_length,
                         truncation=True,
                         padding='max_length',
                         return_token_type_ids=False,
                         return_tensors='tf')

        return tokens
