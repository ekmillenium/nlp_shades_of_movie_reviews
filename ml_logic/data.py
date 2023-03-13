
'''
Import packages
'''

# Basics
import string
import re
import pandas as pd
import sys

# Goggle Cloud
from google.cloud import bigquery

# Relatives
from params import *


def load_data_to_bq(data_size: str, gcp_project: str, bq_dataset: str, table: str, truncate: bool) -> None:
    '''
    Load a dataframe on Big Query
    
    - Read the data from a csv
    - Create a random sample of data from the csv
    - Load the data and create table on Big Query
    '''
    
    data = pd.read_csv('./raw_data/reviews_all.csv')
    
    if data_size != "all":
        data = data.sample(frac=1, replace=True).head(int(data_size))
    
    if data_size == "10000":
        full_table_name = f"{gcp_project}.{bq_dataset}.{table}_10k"
    elif data_size == "300000":
        full_table_name = f"{gcp_project}.{bq_dataset}.{table}_300k"
    elif data_size == "450000":
        full_table_name = f"{gcp_project}.{bq_dataset}.{table}_450k"
    else:
        full_table_name = f"{gcp_project}.{bq_dataset}.{table}_all"
    
    print(f"\nSave data to bigquery {full_table_name}...:")

    # data.columns = [ "_" + str(i) for i in data.columns ] # Avoid TypeError: expected bytes, int or str found
    
    client = bigquery.Client()
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)
    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    res = job.result()

    print(f"Data saved to bigquery, with shape {data.shape}")


class Preprocessing():
    '''
    Preprocessing the data to perform either a NER or BERT model
    '''

    def __init__(self, review: str, model=None):
        self.review = review
        self.model = model

        if model == "bert":
            self.bert()
        elif model == "ner":
            self.ner()
        else:
            print('UnkownModelError: the available models are ["bert","ner"].')


    def ner(self):
        '''
        Function to do the basic data preprocessing for ner model
        - remove the lines about "how many people found this useful" at the end of some reviews
        - remove urls from text
        - remove html tags if there are any
        - remove extra space
        '''
        
        self.review = re.sub("Permalink", "", self.review)
        self.review = re.sub("Was this review helpful?", "", self.review)
        self.review = re.sub("Sign in to vote.", "", self.review)
        self.review = re.sub("\d+ out of \d+ found this helpful", "", self.review)

        self.review = re.sub(r"http\S+", "", self.review)
        
        self.review = re.sub(re.compile('<.*?>'), '', self.review)

        self.review = " ".join(self.review.split())


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
        
        self.review = re.sub("Permalink", "", self.review)
        self.review = re.sub("Was this review helpful?", "", self.review)
        self.review = re.sub("Sign in to vote.", "", self.review)
        self.review = re.sub("\d+ out of \d+ found this helpful", "", self.review)

        self.review = re.sub(r"http\S+", "", self.review)

        self.review = re.sub(re.compile('<.*?>'), '', self.review)

        self.review = self.review.lower()

        self.review = ''.join(char for char in self.review if not char.isdigit())

        for punctuation in string.punctuation:
            self.review = self.review.replace(punctuation, ' ')

        self.review = " ".join(self.review.split())


class TargetBuilder():
    '''
    Class used to add the target columns to the data: the reviews are retrieved as X/10 and can be classed in 2, 3 or 5 classes
    '''
    
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
            return 0


if __name__ == '__main__':
  load_data_to_bq(data_size=sys.argv[2], gcp_project=GCP_PROJECT, bq_dataset=BQ_DATASET, table=f"raw", truncate=True)

