import instaloader
from datetime import datetime, timedelta
from itertools import dropwhile, takewhile
import time

L = instaloader.Instaloader(download_pictures=True, download_videos=False, download_comments=False, save_metadata=True)

username = "username"  # Zamień na swoją nazwę użytkownika
password = "password"  # Zamień na swoje hasło
L.login(username, password)  # Zaloguj się

search = "barcelona"
limit = 500

hashtags = instaloader.Hashtag.from_name(L.context, search).get_posts()

UNTIL = datetime(2023, 7, 24)
SINCE = UNTIL + timedelta(days=1)  # Dodajemy jeden dzień do daty

no_of_downloads = 0
for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, hashtags)):
    if no_of_downloads == limit:
        break
    print(post.date)
    L.download_post(post, "#"+search)
    no_of_downloads += 1
    #time.sleep(2)  # Zwiększyliśmy opóźnienie do 10 sekund między pobraniem postów
