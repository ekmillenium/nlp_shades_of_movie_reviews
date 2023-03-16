
'''
Import packages
'''

# Basics
import streamlit as st
import requests
import pandas as pd
import numpy as np

# Relatives
from interface.main import load_data


#Configuration
st.set_page_config(layout="wide")

#Title
st.markdown("<h1 style='text-align: center; color: black;'>NLP shades of movies</h1>", unsafe_allow_html=True)


st.markdown("<h6 style='text-align: left; color: black;'></h6>", unsafe_allow_html=True)


movie_name = str(st.text_input("Type the name of the movie"))
#scraping to retrieve the id and the image of the movie
###### étapes de scraping

#Create 2 columns to separate the main page
col1, col2 = st.columns([3,7])


if st.button('Search') :
    if movie_name == "":
        st.warning("Please enter a movie name", icon="⚠️")
    else:
        #run the api for the film
        url = "http://localhost:8000/models"
        parameters = {
            'title' : movie_name
            }
        r = requests.get(url, params = parameters).json()
        #Display the poster from the film
        with col1:
        #Display the poster of the movie

            img_url = r['image']
            st.write(img_url)
            st.markdown(f'<img style="width:360px;height:500px;" src={img_url} alt="Poster of the movie">', unsafe_allow_html=True)

        # with col2:
        #     Sentiment, Actors , Summary, Other = st.tabs(["Sentiment analysis on top reviews","Most cited actors","Reviews summary","Other"])
        #     #Sentiment analysis from reviews - with Bert model
        #     with Sentiment:
        #         url = "http://localhost:8000/sentiment-analysis"
        #         parameters = {
        #             'title' : movie_name
        #         }
        #         r = requests.get(url, params = parameters).json()
        #         st.write(r['Rating'])
        #         st.write(r['25 Reviews Model Rating Mean'])
        #         st.write(r['25 Reviews Base Rating Mean'])

        #     with Actors:
        #         url = "http://localhost:8000/extract_entities"
        #         parameters = {
        #             'title' : movie_name
        #         }
        #         r = requests.get(url, params = parameters).json()
        #         st.write(r['People'])

        #     with Summary:
        #         st.markdown('Coming soon...')
        #         # url = "http://localhost:8000/extract_entities"
        #         # parameters = {
        #         #      'title' : movie_name
        #         #  }
        #         # r = requests.get(url, params=parameters).json()
        #         # data = r["People"]
        #         # st.write(data)
        #     with Other:
        #         st.markdown('Coming soon...')


# st.write('test')

# #scraping to retrive the

# if st.button('Rating from reviews'):
#     # print is visible in the server output, not in the page

#     st.write('the rating is ')



# if st.button('NER'):
#     # print is visible in the server output, not in the page

#     st.write('the reviews are')
