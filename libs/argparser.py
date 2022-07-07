import argparse
import logging

def checkthreshold(th):
    try:
        th = float(th)
    except ValueError:
        raise argparse.ArgumentTypeError("%r is not a float value" % th)

    if not 0. <= th <= 1.:
        raise argparse.ArgumentTypeError("%r must be a float between (0.0-1.0)" % th)
    return th

def checkarch(arch):
    archs = ["cnn", "dnn", "rnn"]
    arch = arch.lower()
    if arch is None:
        raise argparse.ArgumentTypeError("ARCH must be one of %r" % {' | '.join(archs.upper())})
    return arch

def checkoptimizer(optimizer):
    optimizers = ["adadelta", "adagrad", "adam", "adamax", "ftrl", "nadam", "rmsprop", "sgd"]
    optimizer = optimizer.lower()
    if optimizer is None:
        raise argparse.ArgumentTypeError("OPTIMIZER must be one of %r" % {' | '.join(optimizer.upper())})
    return optimizer

def checklearningrate(lr):
    try:
        lr = float(lr)
    except ValueError:
        raise argparse.ArgumentTypeError("%r is not a float value" % lr)

    if not 0. < lr < 1.:
        raise argparse.ArgumentTypeError("%r must be a float between (0.0-1.0)" % lr)
    return lr

def checkloglevel(log_level):
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    level = levels.get(log_level.lower())
    if level is None:
        raise argparse.ArgumentTypeError("log level must be one of %r" % {' | '.join(levels.keys())})
    return level

#Default
parser = argparse.ArgumentParser()
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