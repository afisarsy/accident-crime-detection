import argparse
import logging

class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __eq__(self, other):
        return self.start <= other <= self.end
    
    def __repr__(self):
        return "[{0}, {1}]".format(self.start, self.end)

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