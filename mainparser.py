import argparse
from random import choices

from tensorboard import program

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

#subparser mode
subparser_mode = parser.add_subparsers(
    title="Program MODE",
    dest="mode",
    metavar="MODE",
    description="Select Program Mode",
    help=(
        "Available MODE [run, get, test]."
    )
)
subparser_mode.required = True

#Running arguments
parser_run = subparser_mode.add_parser("run", aliases=["RUN"])
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
    "-m",
    "--mic",
    metavar="MIC_INDEX",
    type=int,
    default=0,
    help=(
        "Select used microphone index from available microphone devices. "
        "Use  main.py GET MIC  to get available microphone devices"
    ),
)
parser_run.add_argument(
    "--no-mqtt",
    action="store_true",
    help=(
        "Disable MQTT communication."
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
parser_get = subparser_mode.add_parser('get', aliases=["GET"])
getparams = ["mic", "id"]
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

#Tests arguments
parser_test = subparser_mode.add_parser("test", aliases=["TEST"])
subparser_test = parser_test.add_subparsers(
    title="Unit Test",
    dest="test_mode",
    metavar="NAME",
    description="Select Test NAME",
    help=(
        "Available test NAME [mqtt, gps]."
    )
)
subparser_test.required = True

perser_test_mqtt = subparser_test.add_parser("mqtt", aliases=["MQTT"])
perser_test_mqtt.add_argument(
    "--host",
    metavar="HOST",
    type=str,
    default="localhost",
    help=(
        "Provide MQTT broker hostname or IP address."
    )
)
perser_test_mqtt.add_argument(
    "--port",
    metavar="PORT",
    type=int,
    default=1883,
    help=(
        "Provide MQTT broker Port."
    )
)
perser_test_mqtt.add_argument(
    "topic",
    metavar="TOPIC",
    type=str,
    help=(
        "Provide MQTT topic."
    )
)

parser_test_gps = subparser_test.add_parser("gps", aliases=["GPS"])
parser_test_gps.add_argument(
    "port",
    metavar="PORT",
    help=(
        "Provide serial port."
    )
)
parser_test_gps.add_argument(
    "--baudrate",
    metavar="BAUDRATE",
    type=int,
    default=9600,
    help=(
        "Provide BAUDRATE. "
        "Default 9600"
    )
)

parser_test_inferrt = subparser_test.add_parser("inferrt", aliases=["inference-rt"])
parser_test_inferrt.add_argument(
    "filename",
    metavar="AUDIO_FILE",
    help=(
        "Provide audio file path. "
        "AUDIO_FILE must be a wav file. "
    ),
)
parser_test_inferrt.add_argument(
    "model",
    metavar="MODEL_PATH",
    help=(
        "Provide model path. "
        "MODEL_PATH must contain config.file. "
    ),
)
parser_test_inferrt.add_argument(
    "threshold",
    metavar="TH",
    type=float,
    choices=[Range(0.0, 1.0)],
    help=(
        "Provide threhold value. "
        "TH must be a float between (0.0-1.0). "
    ),
)

parser_test_infer = subparser_test.add_parser("infer", aliases=["inference"])
parser_test_infer.add_argument(
    "models_dir",
    metavar="MODELS_DIR",
    help=(
        "Provide models dir. "
        "MODELS_dir must contain model.h5 and config.file. "
    ),
)