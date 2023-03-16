import streamlit as st
import requests
import pandas as pd



#Configuration
st.set_page_config(layout="wide")

#Title
st.markdown("<h1 style='text-align: center; color: black;'>NLP shades of movies</h1>", unsafe_allow_html=True)


st.markdown("<h6 style='text-align: left; color: black;'>NLP shades of movies2</h6>", unsafe_allow_html=True)


movie_name = str(st.text_input("Type the name of the movie"))
#scraping to retrieve the id and the image of the movie
###### étapes de scraping

#Create 2 columns to separate the main page
col1, col2 = st.columns([3,7])

#Display the poster from the film
with col1:
   #Display the poster of the movie
    img_url = "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_Ratio0.6757_AL_.jpg"
    st.markdown(f'<img style="width:360px;height:500px;" src={img_url} alt="Poster of the movie">', unsafe_allow_html=True)

with col2:
    Sentiment, Actors , Summary, Other = st.tabs(["Sentiment analysis on top reviews","Most cited actors","Reviews summary","Other"])
    #Sentiment analysis from reviews - with Bert model
    with Sentiment:
        st.markdown('Coming soon...')
        # url = "http://localhost:8000/sentiment-analysis"
        # parameters = {
        #     'title' : movie_name
        # }
        # r = requests.get(url, params=parameters).json()
        # data = r['Rating']
        # st.write()
        ########### For visual test only ##################
        data = {
            'id' : [1,2,3,4,5,6,7,8,9,10],
            'model_rate' : [1,0,2,1,1,2,1,0,2,1]
        }

    with Actors:
        st.markdown('Coming soon...')
        # url = "http://localhost:8000/extract_entities"
        # parameters = {
        #      'title' : movie_name
        #  }
        # r = requests.get(url, params=parameters).json()
        # data = r["People"]
        # st.write(data)

    with Summary:
        st.markdown('Coming soon...')
        # url = "http://localhost:8000/extract_entities"
        # parameters = {
        #      'title' : movie_name
        #  }
        # r = requests.get(url, params=parameters).json()
        # data = r["People"]
        # st.write(data)
    with Other:
        st.markdown('Coming soon...')


# st.write('test')

# #scraping to retrive the

# if st.button('Rating from reviews'):
#     # print is visible in the server output, not in the page

#     st.write('the rating is ')



# if st.button('NER'):
#     # print is visible in the server output, not in the page

#     st.write('the reviews are')
