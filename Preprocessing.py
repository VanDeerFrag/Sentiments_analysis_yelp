import re 
from wordcloud import WordCloud 
import nltk 
from nltk import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer


# Cleaning
def clean(txt: str) -> str:

    # Clean balise (html)
    txt = txt.replace('<br />', '')

    # Remove "éèç etc..."
    # txt = re.sub('[^A-Za-z]+', ' ', txt)
    txt = re.sub('[^A-Za-zéèàÿûîêç]+', ' ', txt)
    # txt = re.sub('/^[a-zA-ZÀ-ÿ-. ]*$/', ' ', txt)

    # Remove spaces lower and upper letters
    txt = txt.lstrip().rstrip().lower()
    
    return txt

# Switch with english stopword or french
stop_words = stopwords.words("french") # + stopwords.words('english')         

# Add new stopwords
new_stop_words = ['review', 'un', 'non', 'oui', 'femme', 'date', '#_stars	', 'predicted_sentiment', 'prediction_probability', 'id_business', 'trè', 'une', 'en', 'et', 'le', 'nous', 'je', 'du', 'de']      
stop_words.extend(new_stop_words)                                                      

def remove_stop_words(txt: list) -> list:

    txt = [x for x in txt if x not in stop_words]
    return txt


# Lemmatizer
lemmatizer = WordNetLemmatizer()

def lemmatize(tokens: list) -> list:

    lemmatized_tokens = list(map(lambda x: lemmatizer.lemmatize(x, "v"), tokens))
    lemmatized_tokens = list(map(lambda x: lemmatizer.lemmatize(x, "a"), tokens))
    return lemmatized_tokens



# Regroup fonctions
def preprocess(txt: str, show_progress: bool = False) -> list:

    clean_txt = clean(txt)
    tokens = word_tokenize(clean_txt)
    stop_worded = remove_stop_words(tokens)
    final = lemmatize(stop_worded)

    return final