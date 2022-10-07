import requests as req
import json

BASE_URL1 = "https://imdb-api.com/fr/API/Top250Movies/"
BASE_URL2 = "https://imdb-api.com/fr/API/Wikipedia/"
BASE_URL3 = "https://imdb-api.com/fr/API/Title/"
BASE_URL4 = "https://imdb-api.com/fr/API/YouTubeTrailer/"
BASE_KEY = "YOUR_BASE_KEY"

class InfosMovie:
    
    def __init__(self, rank):
        r = req.get(url = f"{BASE_URL1}{BASE_KEY}/")
        r = r.json()

        movieId = dict(r)["items"][rank - 1]["id"]

        r = req.get(url = f"{BASE_URL2}{BASE_KEY}/{movieId}")
        r = r.json()

        self.frenchTitle = r["titleInLanguage"].split(" (")[0]
        self.rank = rank

        r = req.get(url = f"{BASE_URL3}{BASE_KEY}/{movieId}")
        r = r.json()

        for keys in dict(r):
            setattr(self, keys, r[keys])

        r = req.get(url = f"{BASE_URL4}{BASE_KEY}/{movieId}")
        r = r.json()

        self.trailer = r["videoUrl"]

        #Add Awards

    def saveMovie(self):
        
        with open('utils/data/BDD.json', 'r') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}

        data[self.rank] = [self.frenchTitle, self.image, self.runtimeStr, self.plotLocal, self.directors, self.stars, self.genres, self.trailer, self.releaseDate]

        with open('utils/data/BDD.json', 'w') as f:
            json.dump(data, f)
        

