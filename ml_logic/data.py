
### Import packages ###

# Basics
import string
import re


### Initialize Preprocessing ###

class Preprocessing():
    
    ### Constructor ###
    
    def __init__(self, review: str, model=None):
        self.review = review
        self.model = model
        
        if model == "bert":
            print('BERT preprocessing running ...')
            self.bert()
            print('BERT preprocessing done.')
        elif model == "ner":
            print('NER preprocessing running ...')
            self.ner()
            print('NER preprocessing done.')
        else:
            print('UnkownModelError: the available models are ["bert","ner"].')
    
    
    ### Preprocessing for NER ###
    
    def ner(self):
        # remove the lines about "how many people found this useful" at the end of some reviews
        clean_review = re.sub("Permalink", "", self.review)
        clean_review = re.sub("Was this review helpful?", "", self.review)
        clean_review = re.sub("Sign in to vote.", "", self.review)
        clean_review = re.sub("\d+ out of \d+ found this helpful", "", self.review)

        # Remove urls from text
        clean_review = re.sub(r"http\S+", "", self.review)

        #remove html tags if there are any
        clean_review = re.sub(re.compile('<.*?>'), '', self.review)

        #remove extra space
        clean_review = " ".join(self.review.split())

        return clean_review
    
    
    ### Preprocessing for BERT ###
    
    def bert(self):
        # remove the lines about "how many people found this useful" at the end of some reviews
        clean_review = re.sub("Permalink", "", self.review)
        clean_review = re.sub("Was this review helpful?", "", self.review)
        clean_review = re.sub("Sign in to vote.", "", self.review)
        clean_review = re.sub("\d+ out of \d+ found this helpful", "", self.review)
        
        # Remove urls from text
        clean_review = re.sub(r"http\S+", "", self.review)

        #remove html tags if there are any
        clean_review = re.sub(re.compile('<.*?>'), '', self.review)

        # lowercase characters
        clean_review = self.review.lower()

        # remove numbers
        clean_review = ''.join(char for char in self.review if not char.isdigit())

        # remove punctuation
        for punctuation in string.punctuation:
            clean_review = self.review.replace(punctuation, ' ')

        #remove extra space
        clean_review = " ".join(self.review.split())

        return clean_review
    
    