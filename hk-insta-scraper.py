#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:33:31 2023

@author: lukaszzyla
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:34:38 2023

@author: lukaszzyla
"""

import os
import requests
import json
import mimetypes
from datetime import datetime
import pandas as pd
from hikerapi import Client
import shutil  # Import modułu do przenoszenia plików

# Inicjalizacja klienta hikerapi
cl = Client(token="M6y4xy5oO2dMaroLXpekq7h8lIiyHcya")

# Wczytaj dane z pliku CSV
df = pd.read_csv('hashtags_locations.csv')
hashtags = df['Hashtag'].dropna().tolist()
location_pks = df['Location'].dropna().tolist()

all_media = []

# Pobieranie mediów dla każdego hashtagu
for hashtag in hashtags:
    media_ids_hashtag = cl.hashtag_medias_top_v1(name=hashtag, amount=10)
    all_media.extend(media_ids_hashtag)

# Pobieranie mediów dla każdego PK lokalizacji
for loc_pk in location_pks:
    media_ids_location = cl.location_medias_top_v1(location_pk=loc_pk, amount=10)
    all_media.extend(media_ids_location)

# Definicja zakresu dat
start_date_str = "2023-11-7T00:00:00+00:00"
end_date_str = "2023-11-8T23:59:59+00:00"
start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z')
end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z')

# Przefiltrowanie mediów na podstawie daty "taken_at"
filtered_media = [
    media for media in all_media 
    if isinstance(media, dict) and 'taken_at' in media and start_date <= datetime.strptime(media['taken_at'], '%Y-%m-%dT%H:%M:%S%z') <= end_date
]

media_info_list = []

for media in filtered_media:
    try:
        media_id = media['id']
        file_name = f"{media_id}.json"

        # Zapisz informacje o mediach do pliku JSON
        with open(file_name, 'w') as json_file:
            json.dump(media, json_file, indent=4)

        # Pobierz URL zdjęcia
        image_url = media['image_versions'][0]['url']

        # Pobierz odpowiedź od serwera
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Sprawdź Content-Type w odpowiedzi i mapuj na rozszerzenie
            content_type = image_response.headers['Content-Type']
            extension = mimetypes.guess_extension(content_type) or '.jpg'

            # Pobierz zawartość zdjęcia i zapisz ją do pliku
            image_file_name = f"{media_id}{extension}"
            with open(image_file_name, 'wb') as image_file:
                image_file.write(image_response.content)

            # Dodaj informacje o mediach i nazwie pliku do listy
            media_info_list.append({
                'media_info': file_name,
                'image_file': image_file_name
            })
    except Exception as e:
        print(f"Error processing media {media_id}: {e}")

# Zapisz listę mediów w formie JSON
with open('media_info_list.json', 'w') as json_file:
    json.dump(media_info_list, json_file, indent=4)

# Utwórz folder na zdjęcia i dane
base_folder = os.path.join(os.path.expanduser("~"), "python_spyder", "insta-bcn", "InstagramData")
os.makedirs(base_folder, exist_ok=True)

# Przenieś wszystkie zdjęcia i pliki JSON do folderu
for media_info in media_info_list:
    try:
        image_file_name = media_info['image_file']
        json_file_name = media_info['media_info']
        source_image_path = os.path.join('.', image_file_name)
        source_json_path = os.path.join('.', json_file_name)
        target_image_path = os.path
        target_image_path = os.path.join(base_folder, image_file_name)
        target_json_path = os.path.join(base_folder, json_file_name)
    
    # Użyj shutil.move do przeniesienia plików
        shutil.move(source_image_path, target_image_path)
        shutil.move(source_json_path, target_json_path)
    
    except Exception as e:
        print(f"Error moving files for media {media_info['media_info']}: {e}")

    print("Processing complete. Check the InstagramData folder for files.")

