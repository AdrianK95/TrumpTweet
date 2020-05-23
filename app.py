from flask import Flask, render_template, request

from authen import consumer_key, consumer_secret, access_key, access_secret
import tweepy as tp

#using access keys to twitter app API
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api= tp.API(auth)
#apply app to flask document
app =Flask(__name__)

#query request form
@app.route('/', methods=['GET', 'POST'])
def process_query():
    if request.method == 'POST':
        query = request.form['query']
        
        tweets = api.search(q=query)
        return render_template('results.html', tweets = tweets)
    else:
        return render_template('index.html')

if __name__ == '_main__':
    app.run()
