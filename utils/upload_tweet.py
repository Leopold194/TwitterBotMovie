import urllib.request
import json

from utils.fonctions import cutSummaryIn2, cutSummaryIn3

def upload(api):
    """Start by uploading the mp4 video, then add the description containing the day, title, artist, album, link, and date. 
    Finally, post the tweet, along with the description and media.
    
    Args:
        api : client Twitter
        movieOfDay (dict): all informations about movie of day
    """

    with open('utils/data/BDD.json', 'r') as f:
        data = json.load(f)

    movie_id = list(data.keys())[-1]
    title, poster, time, summary, directors, actors, genres, trailer, date = data[movie_id]

    date = date.split("-")
    date[0], date[2] = date[2], date[0]
    date = "/".join(date)

    hashtag_directors = directors.replace(" ", "").replace("-", "").replace(",", "").replace(".", "")
    hashtag_title = title.replace(" ", "").replace("-", "").replace(",", "").replace(".", "")
    
    urllib.request.urlretrieve(poster, 'uploads/posterOfDay.jpg')

    media = api.media_upload(filename='uploads/posterOfDay.jpg')

    tweet1 = f"🎬 Titre : {title}\n📽️ Réalisateur(s) : {directors}\n👩🏼‍🤝‍👨🏿 Acteurs Principaux : {actors}\n📆 Date de Sortie : {date}\n⏲️ Temps : {time}\n🎭 Genre(s) : {genres}\n🏅 Rang : {movie_id}e\n\n#movie #cinema #{hashtag_title} #{hashtag_directors}"
    
    if len(summary) <= 266:
        tweet2 = f"📜 Synopsis :\n\n{summary}"
    elif 266 < len(summary) <= 510:
        summary = cutSummaryIn2(summary)
        tweet2 = f"📜 Synopsis (Partie 1) :\n\n{summary[0]}"
        tweet3 = f"📜 Synopsis (Partie 2) :\n\n{summary[1]}"
        nb_post = 2
    else:
        summary = cutSummaryIn3(summary)
        tweet2 = f"📜 Synopsis (Partie 1) :\n\n{summary[0]}"
        tweet3 = f"📜 Synopsis (Partie 2) :\n\n{summary[1]}"
        tweet4 = f"📜 Synopsis (Partie 3) :\n\n{summary[2]}"
        nb_post = 3

    tweet5 = f"🎞️ Bande Annonce Officiel :\n\n{trailer}"
    original_tweet = api.update_status(status=tweet1, media_ids=[media.media_id])
    reply1_tweet = api.update_status(status = tweet2, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True)
    if nb_post == 2 or nb_post == 3:
        reply2_tweet = api.update_status(status = tweet3, in_reply_to_status_id=reply1_tweet.id, auto_populate_reply_metadata=True)
        if nb_post == 3:
            reply3_tweet = api.update_status(status = tweet4, in_reply_to_status_id=reply2_tweet.id, auto_populate_reply_metadata=True)
            reply4_tweet = api.update_status(status = tweet5, in_reply_to_status_id=reply3_tweet.id, auto_populate_reply_metadata=True)
        else:
            reply4_tweet = api.update_status(status = tweet5, in_reply_to_status_id=reply2_tweet.id, auto_populate_reply_metadata=True)
    else:
        reply4_tweet = api.update_status(status = tweet5, in_reply_to_status_id=reply1_tweet.id, auto_populate_reply_metadata=True)

    return 1

    
