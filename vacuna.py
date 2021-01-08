# -*- coding: utf-8 -*-



import os, sys
import pandas as pd

bbox = pd.read_csv('bbox_spain.txt')

import tweepy
consumer_key = "XXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXX"

import pandas as pd
import preprocessor as p
import re
ca_df = pd.read_csv('bbox_spain.txt')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

from geopy.geocoders import Nominatim
search= ['Vacuna covid' , 'vacuna coronavirus']
geolocator = Nominatim(user_agent="vacuna_Pablo")
my_path = os.getcwd()
my_path =my_path+'/Tweets/'
if not os.path.exists(my_path):
    os.makedirs(my_path)
   
for i in range(0,17):
  place = bbox['CA'][i]
  geo = geolocator.geocode(place)
  rad = bbox['Radius'][i]
  ruta = my_path+place+'.txt'
  geocode = str (geo.latitude) + ',' + str (geo.longitude) + ',' + str (rad) + 'km'

  for tweet in tweepy.Cursor(api.search, q=search, lang="es", geocode=geocode, tweet_mode='extended', include_rts=False).items(400):
    if (tweet.in_reply_to_status_id_str is None):
      f  = open(ruta, "a") 
      txt = re.sub("RT @[\w]*:","",tweet._json["full_text"])
      regrex_pattern = re.compile(pattern = "["
          u"\U0001F600-\U0001F64F"  # emoticons
          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
          u"\U0001F680-\U0001F6FF"  # transport & map symbols
          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                              "]+", flags = re.UNICODE)
      txt = regrex_pattern.sub(r'',txt)
      txt = re.sub("@[\w]*","",txt)
      txt = re.sub("https?://[A-Za-z0-9./]*","",txt)
      txt = re.sub("\n","",txt)    
      f.write(txt + '\n')
      f.close()

from classifier import SentimentClassifier




sc = SentimentClassifier()
ca = []
polarity = []
for i in range(0,17):
  lugar = bbox['CA'][i]
  ruta = my_path+lugar+'.txt'
  f  = open(ruta, "r")
  p = f.read()
  for j in p.split('\n'):
    #vamos leyendo cada tweet y vamos analizando sentimientos
    polarity.append(sc.predict(j))
    ca.append(lugar)

sentiment = pd.DataFrame([ca,polarity])
sentiment.head()

sentiment = sentiment.T

sentiment.rename(columns={0:'CA',1:'Polaridad'},inplace=True)

sentiment.head()

sentiment['CA'].unique()

import numpy as np
sent = []
for i in sentiment['CA'].unique():
  df = sentiment[sentiment['CA']==i]
  sent.append(np.mean(df['Polaridad']))
sent_array = np.asarray(sent)
sent_array=sent_array+0.2
import matplotlib.pyplot as plt
plt.figure(figsize=(20,8))
mask1 = ((0<=sent_array) & (sent_array<1/3))
mask2 = ((1/3<=sent_array) & (sent_array<=2/3))
mask3 = ((2/3<sent_array) & (sent_array<1))
#plt.bar(range(0,17),sent)
#plt.xticks(np.arange(0, 17),labels=sentiment['CA'].unique())
plt.bar(sentiment['CA'].unique()[mask1],sent_array[mask1], color='red')
plt.bar(sentiment['CA'].unique()[mask2],sent_array[mask2], color='grey')
plt.bar(sentiment['CA'].unique()[mask3],sent_array[mask3], color='green')
plt.show(block=False)



casos = [416724,274817,62950,159615,64751,380406,105977,137410,81706,39030,28590,41847,43361,19139,113863,18765,28045]
poblacion = [6747425,8476718,1504607,5028650,2702244,7652069,2045384,2401230,1330445,1210750,2237309,1061768,656487,315926,2189310,582357,1018775]
vacunados = [2883,25809,442,3252,9124,8150,1983,4846,2004,153,10928,686,1583,324,6000,304,12020]
ratio = [(i / j)*100 for i, j in zip(casos, poblacion)]#covid = pd.DataFrame([casos,poblacion,sent])
ratio_vacu = [(k / l)*100 for k, l in zip(vacunados, poblacion)]

covid = pd.DataFrame([sentiment['CA'].unique(),ratio,ratio_vacu, sent])
covid = covid.T
covid.rename(columns={0:'CA',1:'Ratio contagiados%',2:'Ratio Vacunados %',3:'Polaridad'},inplace=True)
print(covid)



plt.show()
print("FIN DEL PROGRAMA")
