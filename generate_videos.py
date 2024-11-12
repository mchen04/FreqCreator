import os
import openai
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
from time import sleep
from io import BytesIO

# Setup API Key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key

# Paths
audio_folder = "generated_frequencies"     # Folder containing MP3 files
output_folder = "generated_videos"
descriptions_file = "descriptions.txt"     # File to save descriptions
os.makedirs(output_folder, exist_ok=True)

# Function to generate a description using ChatGPT API
def generate_description(frequency):
    prompt = f"Write a calming, informative description about {frequency} Hz frequency and its effects."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    description = response.choices[0].message['content']
    
    # Save the description to a text file
    with open(descriptions_file, "a") as file:
        file.write(f"{frequency} Hz: {description}\n\n")
    
    return description

# Function to generate an AI image using DALL-E based on the frequency
def generate_image(frequency, description):
    prompt = f"Create a calming, abstract visual that represents the relaxing and healing effects of {frequency} Hz frequency. {description}"
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    
    # Download the image
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    
    image_path = os.path.join(output_folder, f"{frequency}Hz_image.jpg")
    image.save(image_path)
    return image_path

# Function to create video with gentle zoom effect
def create_video_with_audio_and_text(audio_path, image_path, description, frequency):
    video_path = os.path.join(output_folder, f"{frequency}Hz_video.mp4")
    
    # Load audio and create ImageClip with text overlay
    audio_clip = AudioFileClip(audio_path).set_duration(300)  # 5 minutes
    image = Image.open(image_path)

    # Add frequency and description text to the image
    draw = ImageDraw.Draw(image)
    title_font = ImageFont.truetype("Roboto-Light.ttf", 60)  # Frequency name font
    desc_font = ImageFont.truetype("Roboto-Light.ttf", 40)   # Description font

    # Set text color (slightly transparent white)
    text_color = (255, 255, 255, 200)

    # Position and draw the frequency title
    frequency_text = f"{frequency} Hz"
    title_position = (50, 50)
    draw.text(title_position, frequency_text, font=title_font, fill=text_color)

    # Position and draw the description text below the frequency title
    desc_position = (50, 130)
    draw.text(desc_position, description, font=desc_font, fill=text_color)

    # Save image with text overlay
    image_with_text_path = os.path.join(output_folder, f"{frequency}Hz_image_with_text.jpg")
    image.save(image_with_text_path)

    # Create video with gentle zoom effect
    image_clip = ImageClip(image_with_text_path).set_duration(300)  # 5 minutes
    zoomed_image_clip = image_clip.fx(vfx.zoom_in, 0.01)  # Gentle zoom effect

    # Combine image and audio
    video = CompositeVideoClip([zoomed_image_clip.set_audio(audio_clip)])
    video.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"Generated video for {frequency} Hz.")

# Main loop: process each MP3 file in the audio folder
for audio_file in os.listdir(audio_folder):
    if audio_file.endswith(".mp3"):
        frequency = audio_file.replace("Hz.mp3", "")
        audio_path = os.path.join(audio_folder, audio_file)

        # Generate description using ChatGPT
        description = generate_description(frequency)
        print(f"Description for {frequency} Hz: {description}")

        # Generate DALL-E image based on frequency
        image_path = generate_image(frequency, description)
        print(f"Generated image for {frequency} Hz.")

        # Create the video with gentle zoom effect and text
        create_video_with_audio_and_text(audio_path, image_path, description, frequency)

        # Optional delay to prevent API rate limiting
        sleep(5)  # Adjust based on rate limits of your APIs
