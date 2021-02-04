import tweepy
import json
import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("uv1ZlOemop7Vw7YTmacb7ECa6", "sHCxECndhAF0xRrFjbuoimHgP9oFi1bd5Yj2WqzhRUD6gUiffd")
auth.set_access_token("795115994868051968-LDVznEIUZLCfyHRiqM9MYGSPhsi5hH9", "8zVGvGyqOx5z3t5A3DZ1WN42tKwuoj6gC47w4VK9JmQhE")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

timeline = api.home_timeline()
"""
for tweet in timeline:
    print(f"{tweet.user.name} said {tweet.text}")

for tweet in api.search(q="elon", lang="en", rpp=10):
    print(f"{tweet.user.name}:{tweet.text}")
"""

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name} : {tweet.text}")

    def on_error(self, status):
        print("Error detected")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["jkuat",], languages=["en"])
