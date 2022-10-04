import os
import sys
import time
import json
import glob
import random
import shutil
import logging

from twitter import tweet_pic


img_dir = "img"
archive_dir = "archive"


def generate_image():

    # loading these is expensive, so only do it if we actually want to generate new images
    from render import render
    from promptgen import promptgen

    os.makedirs(img_dir, exist_ok=True)

    timestamp = int(time.time())
    basename = f"{img_dir}/cthulhu_fhtagn_{timestamp}"

    prompt = promptgen()

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
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s -- %(levelname)s :: %(message)s',
        datefmt='%Y.%m.%dT%H:%M:%S'
    )

    if "--batch" in sys.argv:
        logging.info("generating a batch of images")

        for i in range(2000):
            generate_image()
    else:
        logging.info("tweet an existing image")
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
