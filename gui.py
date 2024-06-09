import pyautogui
import os
import time
import pytesseract
from PIL import ImageEnhance, Image, ImageFilter

import base64
from dotenv import load_dotenv
# import anthropic
from openai import OpenAI

############ SONG RECOMMENDER 2000 ##############

# Function to take a screenshot of the open application
def take_screenshot(file_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)

# Function to encode the image file to base64
def encode_image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# Load environment variables
load_dotenv()

# Initialize the client
# client = anthropic.Anthropic()
client = OpenAI()

##########################

# Optional: Give some delay to switch to the Rekordbox app
time.sleep(5)

# Function to convert time string to seconds
def time_to_seconds(time_str):
    # Replace common OCR misinterpretations
    time_str = time_str.replace('O', '0').replace('I', '1').replace('l', '1').replace('|', '1')
    print(f"Converted time string: {time_str}")

    # Check if the time string is in a common misinterpreted format (e.g., "0444" instead of "04:44")
    if len(time_str) == 4 and ':' not in time_str:
        # Insert a colon between the first two and last two characters
        time_str = time_str[:2] + ':' + time_str[2:]

    # Check if ':' is in the time string
    if ':' in time_str:
        parts = time_str.split(':')
        if len(parts) == 2:
            minutes, seconds = parts
        else:
            # Handle cases where there are more or less parts than expected
            minutes, seconds = '0', '0'
    else:
        # Assume the format is 'MMSS.s' or 'SS.s'
        if len(time_str) > 3:
            minutes, seconds = time_str[:-3], time_str[-3:]
        else:
            minutes, seconds = '0', time_str

    # Convert to integers and handle potential conversion errors
    try:
        minutes = int(minutes)
    except ValueError:
        minutes = 0
    try:
        seconds = float(seconds)
    except ValueError:
        seconds = 0.0

    return minutes * 60 + seconds


# Function to get the hot cue time for a specific deck
def get_hot_cue_time(deck):
    if deck == 1:
        region = (67, 429, 40, 20)  # Coordinates for Deck 1
    else:
        region = (1103, 429, 40, 20)  # Coordinates for Deck 2 (Replace with actual values)
    screenshot = pyautogui.screenshot(region=region)

    # Preprocess the screenshot for better OCR results
    image = screenshot.convert('L')  # Convert to grayscale
    image = ImageEnhance.Contrast(image).enhance(2)  # Increase contrast
    image = image.filter(ImageFilter.EDGE_ENHANCE)  # Apply edge enhancement
    image = image.filter(ImageFilter.SHARPEN)  # Apply sharpening

    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(image, config='--psm 7')
    return text.strip()

# Function to get the current playback position of a specific deck
def get_playback_position(deck):
    if deck == 1:
        region = (523, 301, 60, 20)  # Coordinates for Deck 1
    else:
        region = (1333, 301, 60, 20)  # Coordinates for Deck 2 (Replace with actual values)
    screenshot = pyautogui.screenshot(region=region)

    # Preprocess the screenshot for better OCR results
    image = screenshot.convert('L')  # Convert to grayscale
    image = ImageEnhance.Contrast(image).enhance(2)  # Increase contrast
    image = image.filter(ImageFilter.EDGE_ENHANCE)  # Apply edge enhancement
    image = image.filter(ImageFilter.SHARPEN)  # Apply sharpening

    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(image, config='--psm 7')
    return text.strip()

def has_song_finished(deck):
    # Define the region for the timer of the song based on the deck
    region = (451, 300, 69, 25) if deck == 1 else (1265, 300, 69, 25)
    # Take a screenshot of the defined region
    screenshot = pyautogui.screenshot(region=region)
    # Convert the screenshot to grayscale for better OCR accuracy
    grayscale_image = screenshot.convert('L')
    # Use OCR to read the text from the image
    timer_text = pytesseract.image_to_string(grayscale_image, config='--psm 7').strip()
    # Check if the timer reads "-00:00.0" indicating the song has finished
    return timer_text == "-00:00.0"

# Ensure you have the correct path to tesseract executable
# Example for macOS (if installed via Homebrew)
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Initialize the active deck counter
active_deck = 1

def start_deck(deck):
    if deck == 1:
        pyautogui.press('z')  # Press the key to start Deck 1
        print("Pressed 'z' key to start Deck 1")
    else:
        pyautogui.press('n')  # Press the key to start Deck 2
        print("Pressed 'n' key to start Deck 2")

def press_low_button(deck):
    if deck == 2:
        # Coordinates of the "LOW" button for Deck 2
        low_button_x, low_button_y = 780, 431  # Replace with actual coordinates
    else:
        # Coordinates of the "LOW" button for Deck 1
        low_button_x, low_button_y = 700, 431  # Replace with actual coordinates

    # Move the mouse to the "LOW" button and click
    pyautogui.moveTo(low_button_x, low_button_y, duration=0.1)
    pyautogui.click()
    print(f"Clicked on the 'LOW' button for Deck {deck}")

# Function to load a new song
def load_new_song(deck):
    # Define the file path (replace "rekordbox_screenshot.png" with your actual file path)
    file_path = "rekordbox_screenshot.png"  # or "rekordbox_screenshot.jpeg"

    # Take a screenshot and save it to the specified file path
    take_screenshot(file_path)

    # Encode the image
    encoded_image = encode_image_to_base64(file_path)

    # Create the message
    message = client.chat.completions.create(
    # message = client.messages.create(
        # model="claude-3-haiku-20240307",
        model = "gpt-4-vision-preview",
        max_tokens=2562,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                Analyze the provided image of a DJ software with a playlist of available songs. Your task, as a House and Techno music super fan, is to meticulously extract structured information to create a detailed representation of the songs available for the DJ to play. This includes identifying the track name, the artist's name, the key of the song, the BPM or tempo of the track and the genre. \n\nYour extraction will help in understanding what songs are available for the DJ to select from, facilitating a great party they will play.
                """,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", 
                    "text": "Based on the song that is currently playing (as depicted by the volume bar and the green play button), suggest the next song to play from the playlist shown on the page which would be the best fit. Considerfactors like genre, tempo, key of the track to make your suggestion. Return only the name of the song and nothing else. Ensure to not pick the song that is already playing. Load the title of the song without any inverted commas or brackets. Do not, under any circumstances, make up songs or spellings. Think step by step. Remember that you can't select a song that is not in the playlist. "},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                ],
            },
        ]
)

    # nextsong = message.content[0].text
    nextsong = message.choices[0].message.content

    time.sleep(2)
    # Press space bar
    # pyautogui.press('space')
    # Move to the specific coordinates and click
    pyautogui.moveTo(1315, 607, duration=0.5)
    pyautogui.click()

    time.sleep(0.5)

    pyautogui.typewrite(nextsong)
    pyautogui.moveTo(570, 643, duration=0.5)
    pyautogui.click()
    # Load the track using the appropriate shortcut
    if deck == 1:
        pyautogui.hotkey('shift', 'left')
    else:
        pyautogui.hotkey('shift', 'right')
    # Wait for a second and press space again
    # time.sleep(1)
    # pyautogui.press('space')
    print(f"Loaded new song on Deck {deck}")
    pyautogui.moveTo(1454, 607)
    pyautogui.click()
    pyautogui.moveTo(1020, 540)
    pyautogui.click()

# Press the "LOW" button on the inactive deck immediately
press_low_button(active_deck)

# Define the hot cue B time for the active deck
hot_cue_b_time = get_hot_cue_time(active_deck)
hot_cue_b_seconds = time_to_seconds(hot_cue_b_time)
print(f"Extracted hot cue time: {hot_cue_b_time} ({hot_cue_b_seconds} seconds)")

# Start the initial deck
start_deck(active_deck)

import time

margin_of_error = 0.5  # Example value, set as needed

def check_and_transition(current_deck, current_deck_seconds, hot_cue_b_seconds, next_deck):
    if abs(current_deck_seconds - hot_cue_b_seconds) <= margin_of_error:
        start_deck(next_deck)
        press_low_button(next_deck)
        hot_cue_b_seconds = time_to_seconds(get_hot_cue_time(next_deck))
        return hot_cue_b_seconds
    return hot_cue_b_seconds

def handle_song_finished(deck, next_deck):
    press_low_button(next_deck)
    load_new_song(deck)
    hot_cue_b_seconds = time_to_seconds(get_hot_cue_time(deck))
    return hot_cue_b_seconds

def main_loop():
    hot_cue_b_seconds = 0  # Initialize with a default value or fetch initial hot cue time

    while True:
        deck1_position = get_playback_position(1)
        deck2_position = get_playback_position(2)

        deck1_seconds = time_to_seconds(deck1_position) if deck1_position else None
        deck2_seconds = time_to_seconds(deck2_position) if deck2_position else None

        if deck1_seconds is not None:
            hot_cue_b_seconds = check_and_transition(1, deck1_seconds, hot_cue_b_seconds, 2)

        if deck2_seconds is not None:
            hot_cue_b_seconds = check_and_transition(2, deck2_seconds, hot_cue_b_seconds, 1)

        if has_song_finished(1):
            hot_cue_b_seconds = handle_song_finished(1, 2)

        if has_song_finished(2):
            hot_cue_b_seconds = handle_song_finished(2, 1)

        time.sleep(0.05)

if __name__ == "__main__":
    main_loop()
