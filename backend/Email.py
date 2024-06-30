import sklearn 
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle


def Preprocess(text):

    text=re.sub(r"[^a-zA-Z]", " ", text)
    stop_words=set(stopwords.words("english"))
    words=[word for word in text.split(' ') if word not in stop_words]
    fin=''
    for x in words:
      fin=fin+x+' '

    #words=word_tokenize(text)
    lemma_words = [lemmatizer.lemmatize(o) for o in fin.split(" ")]
    for x in lemma_words:
      fin=fin+x+' '
    return fin


def lowerChange(text):
    return text.lower()
def pre_input(text):
  text_without_linebreaks = text.replace('\n', " ")
  textlower=lowerChange(text_without_linebreaks)
  text_pre=Preprocess(textlower)
  return text_pre

#   TEXT FROM FRONT END HERE

text='''Our biggest sale of the year ends in just a few hours.You can claim 25% off Songcraft Pro by heading to Songcraft right now! 

Not sure why you need Songcraft Pro? You'll get unlimited songs, video collaboration, saved progressions, custom tunings, exclusive songwriting exercises and much more.

We guarantee it will help you write the best songs of your life.

Claim your 25% off!
Enter code BLACKFRIDAY at checkout by 11:59PM on Monday, Nov 27

 to get 25% off a year of Songcraft Pro'''

pro_text=pre_input(text)

loaded_model = pickle.load(open('EMail_Detection_98.pkl', 'rb'))

pred=loaded_model.predict([pro_text])

if pred ==1:
    print("Spam Email Detected")
else:
    print("Safe Email")

