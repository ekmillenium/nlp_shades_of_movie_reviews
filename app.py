
'''
Import packages
'''

# Basics
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# WordCloud
from wordcloud import WordCloud
import plotly.express as px

# Goggle Cloud
from google.cloud import bigquery

# Relatives
from params import *
from interface.main import run_models


#Configuration
st.set_page_config(layout="wide")

with open("style.css") as source:
    st.markdown(f"<style>{source.read()}</style>", unsafe_allow_html=True)

#Title
st.markdown("<h1 class='align text-black'>NLP shades of movies</h1>", unsafe_allow_html=True)

movie_name = str(st.text_input("Which movie do you want to watch?", placeholder="Avatar"))
#scraping to retrieve the id and the image of the movie
###### étapes de scraping

#Create 2 columns to separate the main page
col1, col2 = st.columns([3,7])

if st.button('Search') :
    if movie_name == "":
        st.warning("Please enter a movie name", icon="⚠️")
    else:
        with st.spinner('Analysis in progress...'):
            
            with col1:
                #Display the poster of the movie
                img_url = "https://m.media-amazon.com/images/M/MV5BNjRlZmM0ODktY2RjNS00ZDdjLWJhZGYtNDljNWZkMGM5MTg0XkEyXkFqcGdeQXVyNjAwMjI5MDk@._V1_Ratio0.6757_AL_.jpg"
                st.markdown(f'<img style="width:260px;height:400px;" src={img_url} alt="Poster of the movie">', unsafe_allow_html=True)
            
            #load Big Query
            query = f"""
                SELECT content, title, rating
                FROM {GCP_PROJECT}.{BQ_DATASET}.raw_all
                WHERE tconst = "tt0120755"
                """
            client = bigquery.Client(GCP_PROJECT)
            query_job = client.query(query)
            result = query_job.result()
            data = result.to_dataframe()
            rating = data["rating"].str.replace("/10","").astype(int)
            data = data[rating > 6].head(50)  
                        
            #Results
            df = run_models(df=data)
            ner = df[0]
            bert = df[1]
            bart = df[2]

        st.success('Enjoy! 🎬')
        
        # BERT results
        bert_model_rating = bert['model_rating'].mean()
        
        if bert_model_rating < 0.7:
            sentiment = "Negative 😟"
            sentiment_style = "text-red"
        elif bert_model_rating > 0.7 and bert_model_rating < 1.3:
            sentiment = "Neutral 😐"
            sentiment_style = "text-yellow"
        else:
            sentiment = "Positive 😊"
            sentiment_style = "text-green"
        
        # NER results
        wordcloud = WordCloud().generate(' '.join(ner["people_extracted"].values))
        fig = px.imshow(wordcloud, width=600, height=500)
        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_xaxes(visible=False, showticklabels=False)
        
        with col2:
            Sentiment, Actors , Summary = st.tabs(["Sentiment Analysis","Most Cited Actors","Summary"])
            with Sentiment:
                st.markdown(f"<p class='p-40 {sentiment_style}'>{sentiment}</p>", unsafe_allow_html=True)

            with Actors:
                st.plotly_chart(fig, config={'displayModeBar': False})

            with Summary:
                st.markdown(f"<p class='p-30'>{bart}</p>", unsafe_allow_html=True)
                
