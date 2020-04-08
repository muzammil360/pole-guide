import logging
import logging.handlers
import os
import sys


def get_logger(name, save_dir= "logs", filename="log.txt"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if save_dir and filename:
        # use rotating file handler with each file of size 20 MB and 5 backups
        fh = logging.handlers.RotatingFileHandler(filename=os.path.join(save_dir, filename), maxBytes=20*1024*1024, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
