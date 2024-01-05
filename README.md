# USD-ETS
USD command line tools for the ETS multimedia research lab

# Installation
To install dependencies, run:
```
$ pip install -r requirements.txt
```

# Usage
To display the help menu, run:
```
$ python main.py -h
```
To convert simulation frames output from the PBA Toolkit, for example, run:
```
python ./USD-ETS/main.py -i path/to/pba/frames/ -o animation.usd --fps [#frames per second] --up-axis [Z | Y | X] --from-pba
```
After your USD animation file (`animation.usd`) has been generated, users can generate high-quality renderings of each animation frame (using, for example, [Blender](https://www.blender.org/)). Renderings will typically be output into a sequence of numbered PNG images (i.e. `[frame#].png`). To convert these images into an animated MP4 video, one can run:
```
$ magick.exe mogrify -path path/to/output/ -flatten path/to/rendered/imgs/*.png
$ ffmpeg -r [frame rate] -f image2 -s 1920x1080 -i path/to/output/%04d.png -pix_fmt yuv420p animation.mp4
```
using [ImageMagick](https://imagemagick.org/) and [FFmpeg](https://ffmpeg.org/).
