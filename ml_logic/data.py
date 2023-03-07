import string
import re


def basic_preprocessing(sentence):
    '''
    Function to make the basic preprocessing operations:
    - Remove the text about "how many people found this useful"
    - Remove the html balises if there are any
    - Remove whitespace and extra space
    - Lowercase caracters
    - Remove numbers
    - Remove punctuation
    - Remove url from texts

    '''

    ################## Basic preprocessing #######################################################################
    
    # remove the line about "how many people found this useful" at the end of some reviews
    sentence = re.sub("\d+ out of \d+ found this helpful", "", sentence)
    
    # Remove urls from text
    sentence = re.sub(r"http\S+", "", sentence)
    
    #remove html tags if there are any
    sentence = re.sub(re.compile('<.*?>'), '', sentence)
    
    # lowercase characters
    sentence = sentence.lower()
    
    # remove numbers
    sentence = ''.join(char for char in sentence if not char.isdigit())
    
    # remove punctuation
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, ' ')
    
    #remove extra space
    sentence = " ".join(sentence.split())
    
    return sentence