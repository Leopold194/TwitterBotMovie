import tweepy as tw
import time
import smtplib, ssl

from keep_alive import keep_alive
from datetime import datetime

from utils.upload_tweet import upload
from utils.fonctions import getMovieOfDay
from utils.infos_movie import InfosMovie

consumer_key = "CONSUMER_KEY"
consumer_secret = "CONSUMER_SECRET"

access_token = "ACCESS_TOKEN"
access_token_secret = "ACCESS_TOKEN_SECRET"

"""Used to connect to the Twitter client
"""
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

"""Check if the keys are correct.
"""
try:
    api.verify_credentials()
    print("Bot is online")
    connect = True
except:
    print("Bot has a problem")


keep_alive()
while connect:
    """Check if it's time to post the tweet, especially here 8am"""
    actually_time = datetime.now()
    if (actually_time.hour == 8 and actually_time.minute == 1):
        print("Uploading Tweet ...")
        try:
            movieOfDay = getMovieOfDay()

            movie = InfosMovie(movieOfDay)
            movie.saveMovie()

            time.sleep(3)

            tweet = upload(api)

            if tweet == 1:
                print("Tweet posted")

            time.sleep(60)

        except Exception as Error:
            smtp_address = "smtp.gmail.com"
            smtp_port = 465
            smtp_context = ssl.create_default_context()
            email = "YOUR_PERSONAL_EMAIL"
            password = "YOUR_PASSWORD"

            with smtplib.SMTP_SSL(smtp_address,
                                  smtp_port,
                                  context=smtp_context) as server:
                server.login(email, password)
                server.sendmail(email, "BOT_EMAIL",
                                str(Error))

    else:
        time.sleep(30)
