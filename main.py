import os
import sys
import time
import json
import glob
import random
import shutil

from twitter import tweet_pic


topic = ["ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn", "Iä! Iä! Cthulhu fhtagn!", "a Lovecraftian painting of Cthulhu rising", "Dagon under the sea"]
theme = ["cosmic horror", "lovecraftian", "cyclopean architecture"]
styles = ["photorealistic", "book cover art", "impressionism", "cubism", "steam punk", "cyber punk", "brutalism", "fractal", "abstract", "cave painting", "art nouveau", "octane render", "ultra realistic", "unreal engine", "movie poster", "album cover", "album cover of a death metal band", "comic book illustration", "award winning photography", "made out of Origami", "GTA Vice City, GTA 5 cover art"]
artist = ["by Claude Monet", "by Salvadore Dali", "by Pablo Picasso", "by Piet Mondrian", "by Gustav Klimt", "by Vincent van Gogh", "by Le Corbusier", "drawn by a child", "by Albrecht Dürer", "by HR Giger", "by Tim Burton", "by Frank Miller", "by William Blake", "by Katsushika Hokusai", "by Artgerm", "by Francisco Goya", "by Greg Rutkowski", "by Caspar David Friedrich", "by Bob Ross", "by Zaha Hadid", "by Peter Paul Rubens", "by Pixar", "by Edvard Munch", "by Rembrandt", "by Jeremy Mann", "by Banksy", "by Yayoi Kusama", "by Marc Chagall", "by Leonardo da Vinci", "by Wassily Kandinsky", "by Ted Nasmith", "by Adrian Smith", "by Ernst Haeckel", "by MC Escher", "by John Howe", "by Antoni Gaudi", "by Kim Keever", "by Jessica Rossier", "by Naoto Hattori"]
misc = ["highly detailed", "8k", "elegant", "cinematic lighting", "amazing crisp", "detail no noise", "digital illustration", "digital art", "trending on artstation", "DeviantArt", "intricate", "epic", "high quality", "close up", "character concept art", "beautiful", "eerie", "intricate details", "strong colors", "deep shadows", "sharp focus", "grim dark", "Psychedelic", "super ornate", "complex", "hallucinogen", "mind-blowing", "dreamy", "provenance", "masterpiece", "hypermaximalist", "chaos", "corruption", "colossal", "cinematic", "surreal", "non-euclidean geometry", "intricately detailed", "magnificent", "dynamic lighting", "theme park", "fantastical", "light dust", "diffuse", "grimmer", "orange and teal", "contrast", "volumetric lighting", "triadic colors", "splash art"]

img_dir = "img"
archive_dir = "archive"


def generate_prompt():
    topic_string = [random.choice(topic)]
    theme_string = [] if random.random() < 0.5 else [random.choice(misc)]
    misc_string = random.sample(misc, random.randint(2, 8))

    x = random.random()
    if x < 0.2:
        style_or_artist_string = []
    elif x < 0.6:
        style_or_artist_string = [random.choice(styles)]
    else:
        style_or_artist_string = [random.choice(artist)]

    return ", ".join(topic_string + theme_string + misc_string + style_or_artist_string)


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
