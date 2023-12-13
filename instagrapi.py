#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 09:45:32 2023

@author: lukaszzyla
"""
import time
from instagrapi import Client
from datetime import datetime

# Zastąp dane do logowania swoimi danymi
USERNAME = ''
PASSWORD = ''

# Autentykacja
cl = Client()
cl.login(USERNAME, PASSWORD)

# Zastąp hashtag i daty według potrzeb
HASHTAG = 'barcelona'
START_DATE = datetime(2023, 10, 4)  # RRRR, MM, DD
END_DATE = datetime(2023, 10, 7)  # RRRR, MM, DD

# Pobierz ID dla hashtagu
tag = cl.hashtag_info(HASHTAG)
tag_id = tag.id

print(tag_id)

# Pobierz posty z hashtagu
media_ids = cl.hashtag_medias_recent_v1("barcelona", amount=100)  # Zmodyfikuj "amount" według potrzeb

print(media_ids)

# Filtruj posty na podstawie zakresu dat
filtered_media_ids = []
for media_id in media_ids:
    media = cl.media_info(media_id)
    time.sleep(2)
    media_date = datetime.utcfromtimestamp(media.created_at)
    if START_DATE <= media_date <= END_DATE:
        filtered_media_ids.append(media_id)

# Wyświetl informacje o przefiltrowanych postach
for media_id in filtered_media_ids:
    media = cl.media_info(media_id)
    print(f"Post ID: {media.id}, Created at: {datetime.utcfromtimestamp(media.created_at)}")
