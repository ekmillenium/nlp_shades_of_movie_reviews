
'''
Import packages
'''

# Basics
import pandas as pd

# WordCloud
from wordcloud import WordCloud

# API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Relatives
from interface.main import run_ner_model, run_bart_model, run_bert_model
from scraping.scraper import MovieScrapper
from ml_logic.models import BertModel

# Initialize BERT model
BERT_model = BertModel().load()


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
def extract_entities(title:str):
  '''
  - Scrap the Imdb web site to get the reviews of the movie
  - Convert response to dataframe
  
  - Run NER model
    1- Preprocess the data
    2- Load the pretrained model
    3- Extract entities
    
  - Run BERT model
    1- Preprocess the data
    2- Tokenize the data
    3- Predict sentiment
  '''
  
  df = MovieScrapper("chrome",title).film.reviews
  df = run_ner_model(df=df)
  df.dropna(inplace=True)
  
  df = run_bert_model(model=BERT_model, df=df, base="people")
  people_rating_mean = df["model_rating"].astype(int).mean()
  
  # wordcloud = WordCloud().generate(' '.join(df["content"].values))
  # plt.imshow(wordcloud, interpolation='bilinear')
  # plt.axis("off")
  # plt.show()
  # print(wordcloud.words_)
   
  return {
    "People Model Rating Mean": str(people_rating_mean),
    "People": df["people_extracted"],
    "Content": df["content_extracted"],
    "Content labelized": df["content_extracted_labelized"],
  }


# BART
@app.get("/summarize") # http://localhost:8000/summarize?title=Avatar
def summarize(title:str):
  '''
  - Scrap the Imdb web site to get the reviews of the movie
  - Convert response to dataframe
  - Run NER model
    1- Render str summary
  '''
  
  df = MovieScrapper("chrome",title).film.reviews
  summary = run_bart_model(df=df, model=None)
  
  return {
    "Summarize": summary
  }


# BERT
@app.get("/sentiment-analysis") # http://localhost:8000/sentiment-analysis?title=Avatar
def sentiment_analysis(title:str):
  '''
  Run BERT model
    1- Preprocess the data
    2- Tokenize the data
    3- Predict sentiment
  '''
  
  df = MovieScrapper("chrome",title).film.reviews
  df = run_bert_model(model=BERT_model, df=df)
  model_rating_mean = df["model_rating"].astype(int).mean()
  base_rating_mean = df["rating"].astype(int).mean()
    
  return {
    "Rating": df["model_rating"].astype(str),
    "25 Reviews Model Rating Mean": str(model_rating_mean),
    "25 Reviews Base Rating Mean": str(base_rating_mean)
  }

  

# Root
@app.get("/")
def root():
  return { "Root": "Welcome on NLP shades of movie reviews" }
