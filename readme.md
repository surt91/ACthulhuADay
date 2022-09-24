# :octopus: A Cthulhu A Day

![Example images of Cthulhu](extra/banner.png)

This bot uses Stable Diffusion to tweet a picture of Cthulhu (or one of his friends) each day until the great old one rises. Follow [@ACthulhuADay](https://twitter.com/ACthulhuADay).

## :gear: Setup

We use the the `diffusers` library from huggingface to download the models released by Stable Diffusion.
This requires a huggingface account, to generate an access token (https://huggingface.co/settings/tokens),
which is needed in turn to login via `huggingface-cli login`. (The weights can also be downloaded manually
and the relative path can be passed as `model_id` in `render.py`.)

The dependencies are listed in the `requirements.txt`.

## :art: Usage

Generate many images in the `img/` subfolder:

```bash
python main.py --batch
```

Tweet one of the images in the `img/` subfolder (or generate a new one if `img/` is empty):

```bash
python main.py
```
