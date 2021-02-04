import tweepy
import json
from flask import Flask, render_template, request

app = Flask(__name__)
data = list()

# Authenticate to Twitter
@app.route('/')
def index():
    auth = tweepy.OAuthHandler("uv1ZlOemop7Vw7YTmacb7ECa6", "sHCxECndhAF0xRrFjbuoimHgP9oFi1bd5Yj2WqzhRUD6gUiffd")
    auth.set_access_token("795115994868051968-LDVznEIUZLCfyHRiqM9MYGSPhsi5hH9", "8zVGvGyqOx5z3t5A3DZ1WN42tKwuoj6gC47w4VK9JmQhE")

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # timeline tweets
    timeline_tweets= api.home_timeline()

    # search tweets
    search_tweet = api.search(q="jkuat", lang="en", rpp=10)

    # stream tweets
    class MyStreamListener(tweepy.StreamListener):
        def __init__(self, api):
            self.api = api
            self.me = api.me()

        def on_status(self, tweet):
            print(f"{tweet.user.name} : {tweet.text}")
            t = dict()
            t['name'] = tweet.user.name
            t['text'] = tweet.text
            data.append(t)

        def on_error(self, status):
            print("Error detected")

    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=["trump",], languages=["en"])

    return render_template('home.html', tweets=data)

if __name__=='__main__':
    app.run(debug=True)
