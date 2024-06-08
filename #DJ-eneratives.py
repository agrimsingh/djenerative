import google.generativeai as genai
from PIL import Image
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

genai.configure()

from PIL import Image

image_path = input('Enter the image path (e.g., Rekordbox.jpg): ')
if not os.path.isfile(image_path):
    raise SystemExit("Invalid Image Path!")

img = Image.open(image_path)
img

import time

model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """
You are a DJ that plays house music.

Your inspirations are John Summit, Carl Cox, Mau P, Eric Prydz. You usually like to play sets that are 1-2 hours long and have good transitions and mixing techniques. You usually play between 120-128 bpm.

You need to look from the image of Rekordbox and figure out the next song to play. 

Step 1
Create a list of potential songs based on the ones under "Track Title"

Step 2
Find the songs that are on Deck 1 and Deck 2

Step 3
Remove the songs on Deck and Deck 2 from potential songs

Step 4 
Select the next song from potential songs based on:

Concepts like mixing in key and circles of fifth
Energy matching to make sure the transition to the new song isn't too abrupt
Similar genres
Songs within 124 to 130 bpm

The current song is the one where the play button is green.

Tell me which song I should play next, and return just the next song name
"""

response = model.generate_content([prompt, img])
print('')
print(response.text)
print('-' * 100)
