import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
image_path = "static/temp_image.jpg"

# Diagnostics
print("🧪 Token loaded:", bool(API_TOKEN))
print("📁 Image path exists:", os.path.exists(image_path))

# Exit if .env or image is misconfigured
if not API_TOKEN:
    print("❌ Missing HUGGINGFACE_TOKEN in .env")
    exit()

if not os.path.exists(image_path):
    print("❌ Image not found:", image_path)
    exit()

# Make API request
headers = {"Authorization": f"Bearer {API_TOKEN}"}
url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

with open(image_path, "rb") as f:
    response = requests.post(url, headers=headers, data=f)

print("🔄 Status Code:", response.status_code)

# Print response
try:
    result = response.json()
    print("🧠 Response:", result)
except Exception as e:
    print("❌ Failed to parse JSON:", str(e))
    print("🔍 Raw response:", response.text)
