#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:52:10 2023

@author: lukaszzyla
"""


import os
from google.cloud import vision
import io


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/lukaszzyla/.config/gcloud/application_default_credentials.json"


client = vision.ImageAnnotatorClient()


path = 'park.jpg'
with io.open(path, 'rb') as image_file:
        content = image_file.read()

image = vision.Image(content=content)

response = client.landmark_detection(image=image)
landmarks = response.landmark_annotations
print("Landmarks:")

for landmark in landmarks:
    print(landmark.description)
    for location in landmark.locations:
        lat_lng = location.lat_lng
        print(f"Latitude {lat_lng.latitude}")
        print(f"Longitude {lat_lng.longitude}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
