#(1103, 429, 40, 20)
#(1333, 301, 60, 20)

import pyautogui
import os
import time
import pytesseract
from PIL import ImageEnhance, Image, ImageFilter

# Optional: Give some delay to switch to the Rekordbox app
time.sleep(5)

# Function to convert time string to seconds
def time_to_seconds(time_str):
    # Replace common OCR misinterpretations
    time_str = time_str.replace('O', '0').replace('I', '1').replace('l', '1').replace('|', '1')
    print(f"Converted time string: {time_str}")

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

# Ensure you have the correct path to tesseract executable
# Example for macOS (if installed via Homebrew)
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Initialize the active deck counter
active_deck = 2

def start_deck(deck):
    if deck == 1:
        pyautogui.press('z')  # Press the key to start Deck 1
        print("Pressed 'z' key to start Deck 1")
    else:
        pyautogui.press('n')  # Press the key to stzart Deck 2
        print("Pressed 'n' key to start Deck 2")

def press_low_button(deck):
    if deck == 1:
        # Coordinates of the "LOW" button for Deck 2
        low_button_x, low_button_y = 782, 431  # Replace with actual coordinates
    else:
        # Coordinates of the "LOW" nbutton for Deck 1
        low_button_x, low_button_y = 729, 431  # Replace with actual coordinates

    # Move the mouse to the "LOW" button and click
    pyautogui.moveTo(low_button_x, low_button_y, duration=0.1)
    pyautogui.click()
    print(f"Clicked on the 'LOW' button for Deck {deck}")

# Press the "LOW" button on the inactive deck immediately
press_low_button(active_deck)

# Define the hot cue B time for the active deck
hot_cue_b_time = get_hot_cue_time(active_deck)
hot_cue_b_seconds = time_to_seconds(hot_cue_b_time)
print(f"Extracted hot cue time: {hot_cue_b_time} ({hot_cue_b_seconds} seconds)")

# Start the initial deck
start_deck(active_deck)

# Define the margin of error in seconds
margin_of_error = 0.3  # Since OCR includes tenths of a second, a larger margin might be needed

# Monitor the playback position and switch decks at the cue point
while True:
    playback_position = get_playback_position(active_deck)
    print(f"Current playback position: {playback_position}")

    if playback_position:
        # Convert playback position to seconds
        playback_seconds = time_to_seconds(playback_position)

        # Check if playback position is within the margin of error
        if abs(playback_seconds - hot_cue_b_seconds) <= margin_of_error:
            # Switch to the next deck
            active_deck = 2 if active_deck == 1 else 1
            start_deck(active_deck)

            # Press the "LOW" button on the new inactive deck immediately
            press_low_button(2 if active_deck == 1 else 1)

            # Update hot cue B time for the new active deck
            hot_cue_b_time = get_hot_cue_time(active_deck)
            hot_cue_b_seconds = time_to_seconds(hot_cue_b_time)
            print(f"Updated hot cue time: {hot_cue_b_time} ({hot_cue_b_seconds} seconds)")

    time.sleep(0.1)  # Check every 0.1 seconds
