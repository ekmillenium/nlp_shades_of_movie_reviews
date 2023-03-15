
'''
Import packages
'''

# Basics
import pandas as pd

# API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Relatives
from interface.main import run_ner_model, run_bart_model
from scraping.scraper import MovieScrapper


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
@app.get("/extract_entities") # http://localhost:8000/extract_entities?title=Avatar
def extract_entities(title: str):
  '''
  - Scrap the Imdb web site to get the reviews of the movie
  - Convert response to dataframe
  - Run NER model
    1- Preprocess the data
    2- Load the pretrained model
    3- Extract entities
  '''
  
  df = MovieScrapper("chrome",title).film.reviews
  df = df
  df = run_ner_model(df=df)
  
  return {
    "People": df["people_extracted"],
    "Content": df["content_extracted"],
    "Content labelized": df["content_extracted_labelized"]
  }

@app.get("/summarize") # http://localhost:8000/summarize?title=Avatar
def summarize(title: str):
  '''
  - Scrap the Imdb web site to get the reviews of the movie
  - Convert response to dataframe
  - Run NER model
    1- Render str summary
  '''
  
  df = MovieScrapper("chrome",title).film.reviews
  df = df
  summary = run_bart_model(df=df)
  
  return {
    "Summarize": summary
  }

# Root
@app.get("/")
def root():
  return { "Root": "Welcome on NLP shades of movie reviews" }
