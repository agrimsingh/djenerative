import base64
import pyautogui
from dotenv import load_dotenv
# import anthropic
from openai import OpenAI
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

# Define the file path (replace "rekordbox_screenshot.png" with your actual file path)
# file_path = "rekordbox_screenshot.png"  # or "rekordbox_screenshot.jpeg"
file_path = "rekordbox3.jpeg"

# Take a screenshot and save it to the specified file path
# take_screenshot(file_path)

# Encode the image
encoded_image = encode_image_to_base64(file_path)

# Create the message
message = client.chat.completions.create(
# message = client.messages.create(
    # model="claude-3-haiku-20240307",
    model = "gpt-4-vision-preview",
    max_tokens=2562,
    temperature=0,
    # system="Analyze the provided image of a DJ software with a playlist of available songs. Your task, as a House and Techno music super fan, is to meticulously extract structured information to create a detailed representation of the songs available for the DJ to play. This includes identifying the track name, the artist's name, the key of the song, the BPM or tempo of the track and the genre. \n\nYour extraction will help in understanding what songs are available for the DJ to select from, facilitating a great party they will play.",
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
                "text": "Based on the song that is currently playing (as depicted by the volume bar and the green play button), can you suggest the next song to play from the playlist which would be the best fit? Feel free to consider factors like genre, tempo, key of the track to make your suggestion. Return only the name of the song and nothing else. Ensure to not pick the song that is already playing."},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{encoded_image}",
                },
            ],
        },
        # {
        #     "role": "user",
        #     "content": [
        #         {
        #             "type": "text",
        #             "text": "Based on the song that is currently playing (as depicted by the volume bar and the green play button), can you suggest the next song to play from the playlist which would be the best fit? Feel free to consider factors like genre, tempo, key of the track to make your suggestion. Return only the name of the song and nothing else. Ensure to not pick the song that is already playing."
        #         },
        #         {
        #             "type": "image",
        #             "source": {
        #                 "type": "base64",
        #                 "media_type": "image/png" if file_path.endswith(".png") else "image/jpeg",
        #                 "data": encoded_image
        #             }
        #         }
        #     ]
        # }
    ]
)

print(message.choices[0].message.content)
