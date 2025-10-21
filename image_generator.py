import replicate
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("EXTNREPLICATE")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# --- モデルIDはコードに直接記載 ---
MODEL_ID = "stability-ai/sdxl"

def generate_images(prompt, num_images=1, steps=30, width=512, height=512):
    results = []
    for _ in range(num_images):
        output = replicate.run(
            f"{MODEL_ID}:latest",
            input={
                "prompt": prompt,
                "num_inference_steps": steps,
                "width": width,
                "height": height
            }
        )
        if isinstance(output, list) and output:
            img_url = output[0]
            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))
            results.append(image)
    return results
