import argparse

from libs.argparserbase import checkloglevel, Range

parser = argparse.ArgumentParser(prog="Accident Crime Detection")
parser.add_argument(
    "-log",
    "--log",
    type=checkloglevel,
    default="info",
    help=(
        "Provide logging level. "
        "Example --log debug, default='warning'"
    )
)

#Subparsers
subparsers = parser.add_subparsers(
    title="Program MODE",
    dest="mode",
    metavar="MODE",
    required=True,
    description="Select Program Mode",
    help=(
        "Available MODE [run, get]."
    )
)

#Running arguments
parser_run = subparsers.add_parser("run", aliases=["RUN"])
parser_run.add_argument(
    "model",
    metavar="MODEL_PATH",
    help=(
        "Provide model path. "
        "MODEL_PATH must contain config.file. "
    ),
)
parser_run.add_argument(
    "threshold",
    metavar="TH",
    type=float,
    choices=[Range(0.0, 1.0)],
    help=(
        "Provide threhold value. "
        "TH must be a float between (0.0-1.0). "
    ),
)
parser_run.add_argument(
    "-mic",
    "--mic-index",
    metavar="MIC_INDEX",
    type=int,
    default=0,
    help=(
        "Select used microphone index from available microphone devices. "
        "Use  main.py GET MIC  to get available microphone devices"
    ),
)
parser_run.add_argument(
    "--log-process",
    action="store_true",
    help=(
        "Log processing time into xml file."
    )
)
parser_run.add_argument(
    "-log",
    "--log",
    type=checkloglevel,
    default="info",
    help=(
        "Provide logging level. "
        "Example --log debug, default='warning'"
    )
)

#Get arguments
parser_get = subparsers.add_parser('get', aliases=["GET"])
getparams = ["mic"]
parser_get.add_argument(
    "param",
    metavar="PARAM",
    type=str.lower,
    choices=getparams,
    help=(
        "Provide parameter you want to get. "
        "Available PARAM %s" % {' , '.join(getparams)}
    ),
)