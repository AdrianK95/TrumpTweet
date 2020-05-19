# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:14:44 2020

@author: adrian
"""

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


#read csv into a pandas dataframe separated by ;
trump = pd.read_csv("trump_data.csv", delimiter = ";")

#drop all nan values
trump = trump.dropna()
trump = trump.rename(columns = {"polarity,,,":"polarity"})
trump['text'] = trump['text'].str.replace(r'[^\w\s]+', '')
#trump = trump[~trump.polarity.str.contains("neutral")]
trump['polarity'] = trump['polarity'].str.replace(r'[^\w\s]+', '')

#trump['text'] = trump['text'].
#print(trump.columns)
#tokenise function
def tokenize(text):
    ps = PorterStemmer()
    return [ps.stem(w.lower()) for w in word_tokenize(text)]



#Assigning features x, y
X = trump.text        
y = trump.polarity

#split training and test data
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = .2, random_state = 100)

#transforming data and applying classifer
mlp = Pipeline([('vect', CountVectorizer(ngram_range = (2,2),stop_words = stopwords.words('english'))),('tfidf', TfidfTransformer()), ('mlp', MLPClassifier(alpha=.1, random_state=42, max_iter = 1000))])
#Logreg = Pipeline([('vectorizer', TfidfVectorizer(ngram_range = (1,3), stop_words=stopwords.words('english'), tokenizer=tokenize)), ('classifier', LogisticRegression(solver = 'lbfgs', verbose = 2,C = 100))])

mlp.fit(X_train, y_train)

#Test and training Accuracy 
model = mlp.score(X_test, y_test)
print("The MLP Test Classification Accuracy is:", model )
print("The MLP training set accuracy is : {}".format(mlp.score(X_train,y_train)))
y_pred = mlp.predict(X)

#vadar sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(text):
    for sentence in text:
        score = analyser.polarity_scores(sentence)
        print("{:-<40} {}".format(sentence, str(score)))
        
    
    
sentiment_analyzer_scores(X_test)


