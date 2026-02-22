import torch
from diffusers import StableDiffusionPipeline
import uuid
import os

# Create output directory
OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load model once (cached)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
)
pipe = pipe.to("cpu")  # use CPU (safe for laptops)


def generate_image(prompt: str):
    """
    Generate an image dynamically from text prompt
    """
    image = pipe(
        prompt=prompt,
        num_inference_steps=25,
        guidance_scale=7.5
    ).images[0]

    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    image.save(path)

    return path
