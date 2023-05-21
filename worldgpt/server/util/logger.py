
"""
    Logging functionality.
    Doesn't currently use the name of the class that called it, which in my other tools is pretty handy when working
    with multithreading.
"""


import logging
import os


def init_logging(path: str = os.path.join('worldgpt', 'server', 'persistence', 'log', 'debug.log'), level: int = logging.DEBUG):

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(path),
            logging.StreamHandler()
        ]
    )

