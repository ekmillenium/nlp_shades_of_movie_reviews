
'''
Import packages
'''

# Basics
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Goggle Cloud
from google.cloud import bigquery

# Relatives
from ml_logic.data import Preprocessing, TargetBuilder
from ml_logic.models import NerModel, BertModel, BartModel
from ml_logic.tokenizers import Tokenizer
from params import *

# Model Lifecycle
from prefect import task, flow


# Initialize BERT model
BERT_model = BertModel().load()


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

  return data.head(5)


@task
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

  df["content_extracted_labelized"] = df["content_cleaned"].apply(
    lambda r : NerModel(
      review=r
    ).extract_content_labelized(model)
  )

  df["people_extracted"] = df["content_cleaned"].apply(
    lambda r : NerModel(
      review=r
    ).extract_people(model)
  )

  return df


@task
def run_bert_model(df: pd.DataFrame, model = None, base = None):
  '''
  BERT model with additional layers to make a sentiment classification. The model has already been build and trained

  - Load the model if no model is given in argument
  - Clean the data
  - Predict sentiment (negative, neutral, positive) for each review
  '''

  #Load the model
  if model == None:
      model = BertModel().load()

  #Concatenate the title and the content of the review
  if base == "people":
    df['clean_content'] = df['content_extracted'].astype(str)
  else:
    df['clean_content'] = df['title'].astype(str) + " " +  df['content'].astype(str)

  #Clean the reviews
  df['clean_content'] = df['clean_content'].apply(lambda x: Preprocessing(review = x,model = 'bert').review)

  #Build the rating_3_classes column
  df['rating_3_classes'] = df['rating'].apply(lambda x: TargetBuilder(rating = x,model = 'bert', nb_classes = 3 ).rating).astype('int')

  #Tokenize the data
  tokenizer = Tokenizer()
  tokens = tokenizer.tokenize(list(df['clean_content']))


  #predict the values
  results = model(tokens)
  model_rating = []
  for result in np.array(results):
    model_rating.append(result.argmax())

  #Add the results to 'model_rating' column in data
  df['model_rating'] = model_rating

  return df


@task
def run_bart_model(df: pd.DataFrame):
  '''
  Clean the data and run BART model
  '''
  df['content'] = df['content'].apply(lambda x: Preprocessing(review = x,model = 'bart').review)
  summary = BartModel().get_summary_demo_day(df=df, review_limit=50)
  return summary


@flow(name=PREFECT_FLOW_NAME)
def run_models(df):
  #data_frame = load_data(data_size=sys.argv[1])
  
  ner_result = run_ner_model.submit(df=df) #, wait_for=[data_frame])
  bert_result = run_bert_model.submit(model=BERT_model, df=df) #, wait_for=[data_frame])
  bart_result = run_bart_model.submit(df=df) #, wait_for=[data_frame])
  
  return ner_result.result(), bert_result.result(), bart_result.result()
  


if __name__ == '__main__':
  pass
  #run_models(data_size=sys.argv[1])
