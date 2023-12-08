import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse


def images_to_video(image_folder, video_name, fps, nframes=350, bgcolor=[255,255,255]):
    images = sorted(os.listdir(image_folder), key=lambda x: int(x.split(".")[0]))
    images = [img for img in images if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = frame.shape
    video = cv2.VideoWriter(
        video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )
    for i in range(0, nframes):
        try:
            img_path_1 = os.path.join(image_folder, images[i])
            frame = cv2.imread(img_path_1, cv2.IMREAD_UNCHANGED)
            if frame.shape[2] == 4:
                background = frame[:,:,3] == 0
                for i in range(3):
                    frame[:,:,i][background] = bgcolor[i]
        except:
            break
        video.write(frame[:,:,:3])
    cv2.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PNG to MP4",
        description="""Converts ordered sequence of PNG files into MP4""",
    )
    parser.add_argument(
        "-f", "--folder", 
        default=".", 
        type=str, 
        help="Path containing png image sequence.")
    parser.add_argument("-o", "--output", default="out.mp4", type=str)
    parser.add_argument("--fps", default=20, type=int)
    parser.add_argument("-n", "--nframes", required=True, type=int)
    parser.add_argument("--rename", default=False, type=bool)
    parser.add_argument(
        "--background-color", 
        dest="background_color",
        default="255,255,255", 
        type=str, 
        help="Transforms transparent pixel values to the specified" + 
            " background color. The color is specified in comma-separated RGB values." + 
            " For example specify '--background-color 255,255,255' for a white background.")
    args = parser.parse_args()
    
    if not args.output.endswith(".mp4"):
        print("Output must end with '.mp4'")
        exit()
    
    image_folder = args.folder
    
    if args.rename:
        import re
        import os

        for s in os.listdir(image_folder):
            id = re.findall(r"\d+", s)[-1]
            os.rename(
                os.path.join(image_folder, s),
                os.path.join(image_folder, "{}.png".format(id)),
            )

    fps = args.fps
    bgcolor = [int(s) for s in args.background_color.split(".")]
    images_to_video(image_folder, args.output, fps, nframes=args.nframes, bgcolor=bgcolor)
