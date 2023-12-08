from render_usd import UsdRenderer
import pba

from pxr import Usd

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="USD writer for the ETS multimedia research lab",
        description="""Creates animations in the USD file format.""",
    )
    parser.add_argument("-i", "--input", default=".", type=str, dest="input")
    parser.add_argument("-o", "--output", default="out.usd", type=str, dest="output")
    parser.add_argument("--fps", default=60, type=int, dest="fps")
    parser.add_argument("--up-axis", default="Z", type=str, dest="up_axis")
    parser.add_argument(
        "--from-pba",
        action="store_true",
        dest="from_pba"
    )
    parser.add_argument("--lazy", action="store_true", dest="lazy")
    args = parser.parse_args()
    stage = Usd.Stage.CreateNew(args.output)
    renderer = UsdRenderer(stage, up_axis=args.up_axis, fps=args.fps)

    if args.from_pba:
        pba.render_pba_simulation_to_usd(renderer, args.input, args.lazy, args.fps)

    renderer.save()
        