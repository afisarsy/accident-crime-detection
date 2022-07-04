import argparse

from libs.configLoader import config

schemes = config["schemes"]
parser = argparse.ArgumentParser()

parser.add_argument(
    "scheme",
    type=int,
    choices=range(1, len(schemes)+1),
    metavar="SCHEME_ID",
    help=(
        "Provide scheme index. "
        "Use -get schemes to show available schemes in config.file. "
        "Change scheme parameters from config.file. "
    ),
)

parser.add_argument(
    "-get",
    default=None,
    help=(
        "Provide required data. "
        "Available options [schemes]. "
    )
)  

parser.add_argument(
    "-log",
    "--log",
    default="info",
    help=(
        "Provide logging level. "
        "Example --log debug, default='warning'"
    )
)

options = parser.parse_args()