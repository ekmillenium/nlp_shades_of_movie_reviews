
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
            self.bert()
        elif model == "ner":
            self.ner()
        elif model == "bart":
            self.bart()
        else:
            print('UnknownModelError: the available models are ["bert","ner","bart"].')


    ### Preprocessing for NER ###

    def ner(self):
        '''
        Function to do the basic data preprocessing for ner model
        - remove the lines about "how many people found this useful" at the end of some reviews
        - remove urls from text
        - remove html tags if there are any
        - remove extra space
        '''
        # remove the lines about "how many people found this useful" at the end of some reviews
        self.review = re.sub("Permalink", "", self.review)
        self.review = re.sub("Was this review helpful?", "", self.review)
        self.review = re.sub("Sign in to vote.", "", self.review)
        self.review = re.sub("\d+ out of \d+ found this helpful", "", self.review)

        # Remove urls from text
        self.review = re.sub(r"http\S+", "", self.review)

        #remove html tags if there are any
        self.review = re.sub(re.compile('<.*?>'), '', self.review)

        #remove extra space
        self.review = " ".join(self.review.split())


    ### Preprocessing for BERT ###

    def bert(self):
        '''
        Function to do the basic data preprocessing for BERT model
        - remove the lines about "how many people found this useful" at the end of some reviews
        - remove urls from text
        - remove html tags if there are any
        - remove extra space
        - remove numbers
        - lowercase characters
        - remove punctuation
        '''
        # remove the lines about "how many people found this useful" at the end of some reviews
        self.review = re.sub("Permalink", "", self.review)
        self.review = re.sub("Was this review helpful?", "", self.review)
        self.review = re.sub("Sign in to vote.", "", self.review)
        self.review = re.sub("\d+ out of \d+ found this helpful", "", self.review)

        # Remove urls from text
        self.review = re.sub(r"http\S+", "", self.review)

        #remove html tags if there are any
        self.review = re.sub(re.compile('<.*?>'), '', self.review)

        # lowercase characters
        self.review = self.review.lower()

        # remove numbers
        self.review = ''.join(char for char in self.review if not char.isdigit())

        # remove punctuation
        for punctuation in string.punctuation:
            self.review = self.review.replace(punctuation, ' ')

        #remove extra space
        self.review = " ".join(self.review.split())

    ### Preprocessing for BART summarizer ###

    def bart(self):
        '''
        Function to do the basic data preprocessing for BART model
        - remove the lines about "how many people found this useful" at the end of some reviews
        - remove urls from text
        - remove html tags if there are any
        - remove extra space
        '''
        # remove the lines about "how many people found this useful" at the end of some reviews
        self.review = re.sub("Permalink", "", self.review)
        self.review = re.sub("Was this review helpful?", "", self.review)
        self.review = re.sub("Sign in to vote.", "", self.review)
        self.review = re.sub("\d+ out of \d+ found this helpful", "", self.review)

        # Remove urls from text
        self.review = re.sub(r"http\S+", "", self.review)

        #remove html tags if there are any
        self.review = re.sub(re.compile('<.*?>'), '', self.review)

        #remove extra space
        self.review = " ".join(self.review.split())

class TargetBuilder():
#Class used to add the target columns to the data: the reviews are retrieved as X/10 and can be classed in 2, 3 or 5 classes

### Constructor ###

    def __init__(self, rating: str, model=None, nb_classes = 2):
        self.rating= rating
        self.model = model

        if model == "bert":
            if nb_classes == 2:
                self.bert_two_classes()
            elif nb_classes == 3:
                self.bert_three_classes()
            elif nb_classes == 5:
                self.bert_five_classes()
            else:
                print("The target can only be built for 2, 3 or 5 classes")
        else :
            print('The target builder is only needed for BERT model')


    def bert_two_classes(self):
        '''
        function used to build the target for the BERT model: data is retrieved as a string '9/10' and is transformed
        to 0 if review between 0 and 6 and 1 if review higher than 6
        '''
        # turn rating column into a number between 0 and 10
        number_rating = float(self.rating.replace("/10",""))

        if number_rating > 6:
            self.rating = 1
        else :
            self.rating = 0

    def bert_three_classes(self):
        '''
        function used to build the target for the BERT model: data is retrieved as a string '9/10' and is transformed
        to/
        - 0 if review between 0 and 4
        - 1 if review between 4 and 6
        - 2 if review higher than 6
        '''
        # turn rating column into a number between 0 and 10
        number_rating = float(self.rating.replace("/10",""))

        if number_rating > 6:
            self.rating = 2
        elif number_rating > 4:
            self.rating = 1
        else:
            self.rating = 0

    def bert_five_classes(self):
        '''
        function used to build the target for the BERT model: data is retrieved as a string '9/10' and is transformed
        to/
        - 0 if review between 0 and 2
        - 1 if review between 3 and 4
        - 2 if review between 5 and 6
        - 3 if review between 7 and 8
        - 4 if review between 9 and 10
        '''
        # turn rating column into a number between 0 and 10
        number_rating = float(self.rating.replace("/10",""))

        if number_rating > 8:
            self.rating = 4
        elif number_rating > 6:
           self.rating =  3
        if number_rating > 4:
            self.rating = 2
        elif number_rating > 2:
            self.rating = 1
        else:
            self.rating = 0
