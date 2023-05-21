

from worldgpt.server.util.logger import init_logging
from worldgpt.shared.util.subsystem import Subsystem
from worldgpt.server.subsystem.configuration import Configuration
from worldgpt.server.subsystem.database import Database
from worldgpt.server.subsystem.api import run_in_main_thread


def bootstrap_subsystems():
    """ Instantiates and Bootstraps all subsystems."""
    for subcls in Subsystem.__subclasses__():
        subcls().bootstrap()


def shutdown_subsystems():
    """ Shuts down all subsystems."""
    for subcls in Subsystem.__subclasses__():
        subcls().queue.put(None)


def main():
    init_logging()
    bootstrap_subsystems()
    try:
        while True:
            run_in_main_thread()
    except KeyboardInterrupt:
        shutdown_subsystems()


if __name__ == '__main__':
    main()
