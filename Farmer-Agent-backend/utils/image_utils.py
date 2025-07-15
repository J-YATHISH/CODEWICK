import os
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

# ✅ Load model, processor, tokenizer once (global scope)
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# ⚙️ Generation configuration
gen_kwargs = {"max_length": 20, "temperature": 0.7, "top_p": 0.9, "do_sample": True}


def describe_image(image_file):
    """
    Saves the uploaded image and returns a caption using a local Transformers model.
    """
    try:
        # Save uploaded file
        path = "static/temp_image.jpg"
        image_file.save(path)

        # Load and prepare image
        image = Image.open(path)
        if image.mode != "RGB":
            image = image.convert(mode="RGB")

        pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values.to(device)
        output_ids = model.generate(pixel_values, **gen_kwargs)

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        return preds[0].strip()

    except Exception as e:
        return f"❌ Image captioning failed: {str(e)}"
