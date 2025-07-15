import google.generativeai as genai
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv
import os   

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,  # Fixed typo here
}

safety_settings = [

    {'category': f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT","HATE_SPEECH","DANGEROUS_CONTENT"]
]

model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    generation_config = generation_config,
    safety_settings = safety_settings,
)

def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image : {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def generate_gemini_response(prompt, image_path):
    image_data = read_image_data(image_path)
    response = model.generate_content([prompt, image_data])
    return response.text

input_prompt = (
    "You are a helpful crop expert who speaks simply for rural farmers.\n"
    "This is a plant with... "
    "In very simple and short sentences, explain what this disease is, how it happens, "
    "and how a farmer can treat and stop it. Use easy words any farmer can understand."
)

def process_uploaded_files(files):
    try:
        if not files:
            return None, "No file uploaded."
        file = files[0]
        response = generate_gemini_response(input_prompt, file.name)
        return file, response
    except Exception as e:
        return None, f"Error: {str(e)}"

with gr.Blocks() as demo:
    file_output = gr.Textbox()
    image_output = gr.Image()
    combined_output = [image_output, file_output]
    upload_button = gr.UploadButton(
        "Click to upload an Image",
        file_types=['image'],
        file_count="multiple",
    )
    upload_button.upload(process_uploaded_files, upload_button, combined_output)

demo.launch(debug=True)