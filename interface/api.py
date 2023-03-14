
'''
Import packages
'''

# Basics
import pandas as pd

# API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Relatives
from interface.main import run_ner_model

# Spacy 
import spacy
from spacy import displacy


'''
Middlewares
'''

app = FastAPI()

# Optional, good practice for dev purposes. Allow all middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

'''
Specifications
'''

# NER (extract entities)
@app.get("/extract_entities") # http://localhost:8000/extract_entities?title=Pulp%20Fiction
def extract_entities(title: str):
  '''
  - Scrap the Imdb web site to get the reviews of the movie
  - Convert response to dataframe
  - Run NER model
    1- Preprocess the data
    2- Load the pretrained model
    3- Extract entities
  '''
  ### SCRAPER HERE ###
  pass

  df = pd.read_csv('./raw_data/reviews_10k.csv')
  df = df.head(2)
  df = run_ner_model(df=df)
  
  return {
    "Content": df["content_extracted"],
    "Content labelized": df["content_extracted_labelized"]
  }


# Root
@app.get("/")
def root():
  return { "Root": "Welcome on NLP shades of movie reviews" }
