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