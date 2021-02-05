import tweepy
import json
import sqlite3 as sql
from flask import Flask, render_template, request, g


app = Flask(__name__)

conn = sql.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS tweets (id INTEGER PRIMARY KEY, name TEXT, text TEXT)')
conn.close()



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
            try:
                name = tweet.user.name
                text = tweet.text

                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO tweets (name,text) VALUES (?,?)",(name,text) )

                    con.commit()
                    msg = "Record successfully added"
            except:
                con.rollback()
                msg = "error in insert operation"

            finally:
                return render_template("home.html")
                con.close()

        def on_error(self, status):
            print("Error detected")

    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=["trump",], languages=["en"])
    return render_template('home.html')


@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("select * from tweets order by id DESC")

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


if __name__=='__main__':
    app.run(debug=True)
