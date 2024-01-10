from openai import OpenAI
import base64
import errno
from elevenlabs import generate, play, set_api_key
from pynput import keyboard
import cv2
import time
from PIL import Image
import numpy as np
import os
import pyautogui

OAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OAI_API_KEY)

set_api_key(os.environ.get("ELEVEN_API_KEY"))

# Folder
folder = "frames"

# Create the frames folder if it doesn't exist
frames_dir = os.path.join(os.getcwd(), folder)
os.makedirs(frames_dir, exist_ok=True)


def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)


def play_audio(text):
    audio = generate(text=text,
                     voice=os.environ.get("ELEVENLABS_VOICE_ID"),
                     model="eleven_multilingual_v2")

    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = "narration"
    file_path = os.path.join(dir_path, f"{unique_id}.wav")

    with open(file_path, "wb") as f:
        f.write(audio)

    play(audio)
    os.remove(file_path)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def analyze_image(base64_image):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
                     {
                         "role": "system",
                         "content": """
                You are a famous Geosuessr player Trevor Rainbolt. 
                You see a screenshot from a Geoguessr game. 
                Act like you are playing this game on Twitch and comment on it.
                If you see the gameplay: Tell us your thought process. Make it short. Two sentences maximum. 
                Tell us what country and area we are in given the visual clues. 
                Don't repeat yourself. Make it informal.
                If you see the result screen: Comment on the score only. If the guess score is over 4000, say `Nice`, or `I'll take it`, or `Close enough`, or `That was easy`.
                """,
                     },
                 ]
                 + generate_new_line(base64_image),
        max_tokens=256,
    )
    response_text = response.choices[0].message.content
    return response_text


def on_release(key):
    if key == keyboard.Key.space:
        # Execute the main function
        execute()

    if key == keyboard.Key.esc:
        # Stop listener
        return False


def capture_screen():
    # Capture the screen
    frame = pyautogui.screenshot()

    # Convert the frame to a PIL image
    pil_img = Image.fromarray(np.array(frame))

    # Convert the PIL image back to an OpenCV image
    frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Save the frame as an image file
    print("📸 Let's go! Saving screenshot.")
    path = f"{folder}/frame.jpg"
    cv2.imwrite(path, frame)


def execute():

    # Wait for 3 seconds
    time.sleep(3)

    # Make a screenshot
    capture_screen()

    # Path to the image
    image_path = os.path.join(os.getcwd(), "frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # Analyze image
    print("👀 Trevor is watching...")
    analysis = analyze_image(base64_image)

    print("🎙️ Trevor says:")
    print(analysis)

    play_audio(analysis)


def main():
    # Collect spacebar clicks
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
