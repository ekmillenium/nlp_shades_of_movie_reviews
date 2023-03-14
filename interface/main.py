
'''
Import packages
'''

# Basics
import pandas as pd
import sys
from pathlib import Path

# Goggle Cloud
from google.cloud import bigquery

# Relatives
from ml_logic.data import Preprocessing
from ml_logic.models import NerModel, BertModel
from ml_logic.tokenizers import Tokenizer
from params import *


def load_data(data_size: str):
  '''
  Load the data from a local csv or from Querying Big Query server
  '''

  data_query_cache_path = Path(LOCAL_DATA_PATH).joinpath("raw_data", f"reviews_{data_size}.csv")
  data_query_cached_exists = data_query_cache_path.is_file()

  query = f"""
    SELECT *
    FROM {GCP_PROJECT}.{BQ_DATASET}.raw_{data_size}
    """

  if data_query_cached_exists:
    print('---------------------------')
    print("Load data from local CSV...")
    print('---------------------------')
    data = pd.read_csv(data_query_cache_path)
  else:
    print('-------------------------------------------')
    print("Load data from Querying Big Query server...")
    print('-------------------------------------------')
    client = bigquery.Client(GCP_PROJECT)
    query_job = client.query(query)
    result = query_job.result()
    data = result.to_dataframe()

    data.to_csv(data_query_cache_path, header=True, index=False) # Save it locally to accelerate for next queries!

  return data


def run_ner_model(df: pd.DataFrame):
  '''
  Named Entity Recognition (NER) model

  - Clean the data
  - Load the pretrained model
  - Extract information from NER
  '''

  df["content_cleaned"] = df["content"].apply(
    lambda r : Preprocessing(
      model="ner",
      review=r,
    ).review
  )

  model = NerModel(pretrained_model="en_core_web_trf").load()

  df["content_extracted"] = df["content_cleaned"].apply(
    lambda r : NerModel(
      review=r
    ).extract_content(model)
  )

  df["people_extracted"] = df["content_cleaned"].apply(
    lambda r : NerModel(
      review=r
    ).extract_people(model)
  )

  return df


def run_bert_model(df: pd.DataFrame):
  '''
  BERT model with additional layers to make a sentiment classification. The model has already been build and trained

  - Clean the data
  - Load the pretrained model
  - Predict sentiment (negative, neutral, positive) for each review
  '''

  #Concatenate the title and the content of the review
  df['clean_content'] = df['title'].astype(str) + " " +  df['content'].astype(str)

  #Clean the reviews
  df['clean_content'] = df['clean_content'].apply(lambda x: Preprocessing(review = x,model = 'bert').review)


  #Tokenize the data
  tokenizer = Tokenizer()
  tokens = tokenizer.tokenize(list(df['clean_content']))

  print(tokens)

  #Load the pretrained model
  model = BertModel()
  model.load()

#predict the value
  result = model.predict(tokens)


  return result






if __name__ == '__main__':
  df = load_data(data_size=sys.argv[2])
  run_ner_model(df=df)
