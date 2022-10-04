import os
import time
import json
import glob
import random
import shutil
import logging
import argparse

from twitter import tweet_pic


img_dir = "img"
archive_dir = "archive"


def generate_image(topic=None, steps=None):

    # loading these is expensive, so only do it if we actually want to generate new images
    from render import render
    from promptgen import promptgen

    os.makedirs(img_dir, exist_ok=True)

    timestamp = int(time.time())
    basename = f"{img_dir}/cthulhu_fhtagn_{timestamp}"

    prompt = promptgen(topic)

    options = {
        "prompt": prompt,
        "basename": basename,

        "seed": timestamp,
        "height": 512,
        "width": 512,

        "num_inference_steps": 150 if steps is None else steps,
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
        format="%(asctime)s -- %(levelname)s :: %(message)s",
        datefmt="%Y.%m.%dT%H:%M:%S"
    )

    parser = argparse.ArgumentParser(description="Generate images")
    parser.add_argument(
        "--batch",
        action="store_true",
        help="generate a batch of random images"
    )
    parser.add_argument(
        "--topic",
        default=None,
        help="topic of generated image"
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=1,
        help="number of images to generate"
    )
    parser.add_argument(
        "-s",
        "--steps",
        type=int,
        default=50,
        help="number of inference steps of Stable Diffusion"
    )

    args = parser.parse_args()

    if args.batch or args.topic:
        logging.info(f"generating a batch of {args.num} images, given topic: {args.topic}")

        for i in range(args.num):
            generate_image(args.topic, steps=args.steps)
    else:
        logging.info("tweet an existing image")
        try:
            txtname = random.choice(glob.glob(f"{img_dir}/*.txt"))
            filename = txtname.replace(".txt", ".png")
        except IndexError:
            _, filename = generate_image(steps=args.steps)
            txtname = filename.replace(".png", ".txt")

        with open(txtname) as f:
            d = json.loads(f.read())
            prompt = d["prompt"]

        tweet_image(prompt, filename)

        archive_dir = "archive"
        os.makedirs(archive_dir, exist_ok=True)
        shutil.move(txtname, txtname.replace(img_dir, archive_dir))
        shutil.move(filename, filename.replace(img_dir, archive_dir))
