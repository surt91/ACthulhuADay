import os
import sys
import time
import json
import glob
import random
import shutil

from twitter import tweet_pic


styles = ["photorealistic", "book cover art", "impressionism", "cubism", "steam punk", "brutalism", "fractal", "abstract", "cave painting"]
misc = ["highly detailed", "8k", "elegant", "cinematic lighting", "amazing crisp", "detail no noise", "DOF", "digital illustration", "digital art", "trending on artstation", "intricate", "epic", "high quality", "high detail", "close up", "character concept art"]
theme = ["cosmic horror"]
topic = ["Cthulhu fhtagn", "ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn", "Iä! Iä! Cthulhu fhtagn!"]
# choose one 50% of the time
artist = ["by Monet", "by Salvadore Dali", "by Pablo Picasso", "by Mondrian", "by Klimt", "by van Gogh", "by le Corbusier", "drawn by a child"]

img_dir = "img"
archive_dir = "archive"


def generate_prompt():
    style_string = [] if random.random() < 0.5 else [random.choice(styles)]
    misc_string = random.sample(misc, random.randint(4, 8))
    theme_string = [] if random.random() < 0.5 else [random.choice(misc)]
    topic_string = [random.choice(topic)]
    artist_string = [] if random.random() < 0.5 else [random.choice(artist)]

    return ", ".join(topic_string + theme_string + misc_string + style_string + artist_string)


def generate_image():

    os.makedirs(img_dir, exist_ok=True)

    timestamp = int(time.time())
    basename = f"{img_dir}/cthulhu_fhtagn_{timestamp}"

    prompt = generate_prompt()

    options = {
        "prompt": prompt,
        "basename": basename,

        "seed": timestamp,
        "height": 512,
        "width": 512,

        "num_inference_steps": 150,
    }

    filename = render(**options)

    with open(basename + ".txt", "w") as f:
        f.write(json.dumps(options, indent=2))

    return prompt, filename


def tweet_image(prompt, filename):
    tweet_pic(path=filename, text=prompt)


if __name__ == "__main__":
    if "--batch" in sys.argv:
        from render import render
        for i in range(2000):
            generate_image()
    else:
        try:
            txtname = random.choice(glob.glob(f"{img_dir}/*.txt"))
            filename = txtname.replace(".txt", ".png")
        except IndexError:
            _, filename = generate_image()
            txtname = filename.replace(".png", ".txt")

        with open(txtname) as f:
            d = json.loads(f.read())
            prompt = d["prompt"]

        tweet_image(prompt, filename)

        archive_dir = "archive"
        os.makedirs(archive_dir, exist_ok=True)
        shutil.move(txtname, txtname.replace(img_dir, archive_dir))
        shutil.move(filename, filename.replace(img_dir, archive_dir))
