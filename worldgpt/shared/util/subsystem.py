

"""
    Part of my standard program design pattern, usually instantiated as a singleton,
    class properties are by convention only written to by the class that owns it,

    Objects are typically stored as dataclasses in my tools now, so you can provide a copy of the dataclass to the
    Subsystem queue and it will be processed by the worker, and subsequently written to the property that stores it.

"""


import abc
import logging
import queue
import threading
from typing import Union
from worldgpt.shared.util.rwlock import RWLock


class Subsystem:
    """
        Subsystem class, a multipurpose controller class that's designed to centralise functionality for the program.
        The lock property is designed for use with the RWLock object, but can be used with a standard threading.Lock
    """

    def __init__(self):
        self.lock: RWLock = RWLock()
        self.queue: queue.Queue = queue.Queue()
        self.worker: threading.Thread = threading.Thread(target=self.do_work, name=f'{self.__class__.__name__}_worker')
        self.active: bool = False

    def first_run(self):
        """ Ran when the bootstrap method determined that this is the first time this subsystem has been run. """
        pass

    def bootstrap(self):
        """ The main function typically instantiates the subsystem by calling this method.

            This method should at the very least:
                1. determine it's initial configuration.py.py.py by retrieving it from a persistent store or configuration.py.py.py
                    subsystem.
                2. determine if it's the first run of this subsystem, and if so, call the first_run method.
                3. set the active flag to True
                4  call the worker's `start` method.
        """
        logging.info(f'bootstrapping {self.__name__} Subsystem')
        self.active = True
        self.worker.start()

    def do_work(self):
        """ This is the worker thread's target. by convention if the class recieves a Nonetype object it should treat
            that as a signal for graceful shutdown.

            The queue should accept a dataclass of an object it's responsible for processing. the worker consumes the
            queue and processes it accordingly.
        """
        while self.active:
            task = self.queue.get()
            if task is None:
                self.shutdown()
                break

    def shutdown(self):
        """ Responsible for graceful shutdown of the Subsystem components. """
        logging.info(f'{self.__class__.__name__} gracefully shutting down.')
        self.active = False
        try:
            self.worker.join()
        except Exception as e:
            logging.error(e)
            pass
