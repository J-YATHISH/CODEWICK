import os
from dotenv import load_dotenv
import requests
from PIL import Image

# Load environment variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def describe_image(image_file):
    """
    Saves the uploaded image and sends it to Hugging Face BLIP captioning API.
    Returns the generated image description.
    """

    path = "static/temp_image.jpg"
    image_file.save(path)

    # BLIP model endpoint
    url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

    try:
        with open(path, "rb") as f:
            response = requests.post(url, headers=headers, data=f)
            response.raise_for_status()
            return response.json()[0]['generated_text']
    except Exception as e:
        return f"❌ Image captioning failed: {str(e)}"
