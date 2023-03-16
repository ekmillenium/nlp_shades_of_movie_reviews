
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

@app.get("/models") # http://localhost:8000/models?title=Avatar
def run_models(title:str):
  '''
  - Scrap the Imdb web site to get the reviews of the movie
  - Convert response to dataframe
  - Run all models
  '''
  film = MovieScrapper("chrome",title).film
  data = film.reviews
  image_url = film.image

############## run NER model ##########################################################################################
    # 1- Preprocess the data
    # 2- Load the pretrained model
    # 3- Extract entities

  df_ner = data.copy()
  df_ner = run_ner_model(df=df_ner)
  df_ner.dropna(inplace=True)

  df_ner = run_bert_model(model=BERT_model, df=df_ner, base="people")
  people_rating_mean = df_ner["model_rating"].astype(int).mean()

############## run BART model ##########################################################################################
    # 1- Render str summary

#   summary = run_bart_model(df=data)


############## run BERT model ##########################################################################################
    # 1- Preprocess the data
    # 2- Tokenize the data
    # 3- Predict sentiment


  df_bert = run_bert_model(model=BERT_model, df=data)
  model_rating_mean = df_bert["model_rating"].astype(int).mean()
  base_rating_mean = df_bert["rating"].astype(int).mean()



#Returns for all models

  return {
    # returns the image of the film
    "image" : image_url,
    # returns for ner
    "People Model Rating Mean": str(people_rating_mean),
    "People": df_ner["people_extracted"],
    "Content": df_ner["content_extracted"],
    "Content labelized": df_ner["content_extracted_labelized"],
    # # returns for bart
    # "Summarize": summary,
    ## returns for bert
    "Rating": df_bert["model_rating"].astype(str),
    "25 Reviews Model Rating Mean": str(model_rating_mean),
    "25 Reviews Base Rating Mean": str(base_rating_mean)
  }


# Root
@app.get("/")
def root():
  return { "Root": "Welcome on NLP shades of movie reviews" }
