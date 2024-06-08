import pyautogui
import os
import time
import pytesseract
from PIL import ImageEnhance, Image, ImageFilter

# Optional: Give some delay to switch to the Rekordbox app
time.sleep(5)

# Function to convert time string to seconds
def time_to_seconds(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
    else:
        minutes, seconds = parts[0], '0'
    return int(minutes) * 60 + float(seconds)

# Function to get the hot cue time
def get_hot_cue_time():
    region = (67, 429, 40, 20)  # Replace with actual coordinates and size
    screenshot = pyautogui.screenshot(region=region)

    # Preprocess the screenshot for better OCR results
    image = screenshot.convert('L')  # Convert to grayscale
    image = ImageEnhance.Contrast(image).enhance(2)  # Increase contrast
    image = image.filter(ImageFilter.EDGE_ENHANCE)  # Apply edge enhancement
    image = image.filter(ImageFilter.SHARPEN)  # Apply sharpening

    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(image, config='--psm 7')
    return text.strip()

# Function to get the current playback position of Deck 1
def get_playback_position():
    region = (523, 301, 60, 20)  # Replace with actual coordinates and size
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

# Press the "z" key to start the song on Deck 1
pyautogui.press('z')
print("Pressed 'z' key to start Deck 1")

# Define the hot cue B time
# hot_cue_b_time = "04:45"  # Replace with the actual time format
hot_cue_b_time = get_hot_cue_time()
hot_cue_b_seconds = time_to_seconds(hot_cue_b_time)
print(f"Extracted hot cue time: {hot_cue_b_time} ({hot_cue_b_seconds} seconds)")


# Coordinates of the "LOW" button for Deck 2
low_button_x_deck2, low_button_y_deck2 = 780, 431  # Replace with actual coordinates

# Move the mouse to the "LOW" button and click
pyautogui.moveTo(low_button_x_deck2, low_button_y_deck2, duration=0.5)
pyautogui.click()
print("Clicked on the 'LOW' button for Deck 2")

# Define the margin of error in seconds
margin_of_error = 0.3  # Since OCR includes tenths of a second, a larger margin might be needed


# Monitor the playback position and trigger Deck 2 at the cue point
while True:
    playback_position = get_playback_position()
    print(f"Current playback position: {playback_position}")
   
    if playback_position:
        # Convert playback position to seconds
        playback_seconds = time_to_seconds(playback_position)

        # Check if playback position is within the margin of error
        if abs(playback_seconds - hot_cue_b_seconds) <= margin_of_error:
            pyautogui.press('n')  # Press the key to start Deck 2
            print("Pressed 'n' key to start Deck 2 at hot cue B")

            break

    time.sleep(0.1)  # Check every 0.1 seconds

# Optional: Add a small delay to ensure Deck 2 starts
time.sleep(2)
