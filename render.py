import logging

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"

logging.info(f"load {model_id}")
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, use_auth_token=True)
pipe = pipe.to(device)


def render(prompt, basename, height=512, width=512, seed=42, num_inference_steps=50):

    logging.info(f"start rendering: {height}x{width} over {num_inference_steps} steps, seed = {seed}")

    filename = basename + ".png"

    generator = torch.Generator("cuda").manual_seed(seed)

    with autocast("cuda"):
        image = pipe(prompt, num_inference_steps=num_inference_steps, generator=generator, height=height, width=width)["sample"][0]
        image.save(filename)

    return filename
