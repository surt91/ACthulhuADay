import random
import logging

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


topic = ["ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn", "Iä! Iä! Cthulhu fhtagn!", "a Lovecraftian painting of Cthulhu rising", "Dagon under the sea"]
theme = ["cosmic horror", "lovecraftian", "cyclopean architecture"]
styles = ["photorealistic", "book cover art", "impressionism", "cubism", "steam punk", "cyber punk", "brutalism", "fractal", "abstract", "cave painting", "art nouveau", "octane render", "ultra realistic", "unreal engine", "movie poster", "album cover", "album cover of a death metal band", "comic book illustration", "award winning photography", "made out of Origami", "GTA Vice City, GTA 5 cover art"]
artist = ["by Claude Monet", "by Salvadore Dali", "by Pablo Picasso", "by Piet Mondrian", "by Gustav Klimt", "by Vincent van Gogh", "by Le Corbusier", "drawn by a child", "by Albrecht Dürer", "by HR Giger", "by Tim Burton", "by Frank Miller", "by William Blake", "by Katsushika Hokusai", "by Artgerm", "by Francisco Goya", "by Greg Rutkowski", "by Caspar David Friedrich", "by Bob Ross", "by Zaha Hadid", "by Peter Paul Rubens", "by Pixar", "by Edvard Munch", "by Rembrandt", "by Jeremy Mann", "by Banksy", "by Yayoi Kusama", "by Marc Chagall", "by Leonardo da Vinci", "by Wassily Kandinsky", "by Ted Nasmith", "by Adrian Smith", "by Ernst Haeckel", "by MC Escher", "by John Howe", "by Antoni Gaudi", "by Kim Keever", "by Jessica Rossier", "by Naoto Hattori"]
misc = ["highly detailed", "8k", "elegant", "cinematic lighting", "amazing crisp", "detail no noise", "digital illustration", "digital art", "trending on artstation", "DeviantArt", "intricate", "epic", "high quality", "close up", "character concept art", "beautiful", "eerie", "intricate details", "strong colors", "deep shadows", "sharp focus", "grim dark", "Psychedelic", "super ornate", "complex", "hallucinogen", "mind-blowing", "dreamy", "provenance", "masterpiece", "hypermaximalist", "chaos", "corruption", "colossal", "cinematic", "surreal", "non-euclidean geometry", "intricately detailed", "magnificent", "dynamic lighting", "theme park", "fantastical", "light dust", "diffuse", "grimmer", "orange and teal", "contrast", "volumetric lighting", "triadic colors", "splash art"]

model_id = "Gustavosta/MagicPrompt-Stable-Diffusion"

logging.info(f"load {model_id}")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)


def promptgen_ai(start):
    logging.info("generate a prompt using an AI")

    generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
    prompt = generator(start, max_length=60, num_return_sequences=1)

    prompt = prompt[0]["generated_text"]

    logging.info(f"prompt: '{prompt}'")

    return prompt


def promptgen_manual(topic_string):
    logging.info("generate a simple prompt with random keywords")
    x = random.random()
    if x < 0.2:
        style_or_artist_string = []
    elif x < 0.6:
        style_or_artist_string = [random.choice(styles)]
    else:
        style_or_artist_string = [random.choice(artist)]
    theme_string = [] if random.random() < 0.5 else [random.choice(misc)]
    misc_string = random.sample(misc, random.randint(2, 8))

    prompt = ", ".join([topic_string] + theme_string + misc_string + style_or_artist_string)

    logging.info(f"prompt: '{prompt}'")

    return prompt


def promptgen():
    topic_string = random.choice(topic)

    if random.random() < 0.5:
        prompt = promptgen_ai(topic_string)
    else:
        prompt = promptgen_manual(topic_string)

    return prompt


if __name__ == "__main__":
    promptgen_ai("a Lovecraftian painting of Cthulhu rising")
