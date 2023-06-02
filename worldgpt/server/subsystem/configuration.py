

import json
import logging
import os
from typing import Union
from pydantic import DirectoryPath, FilePath, IPvAnyAddress, conint
from worldgpt.server.model.configuration import ServerConfiguration
from worldgpt.shared.util import about
from worldgpt.shared.util.singleton import Singleton
from worldgpt.shared.util.subsystem import Subsystem


class Configuration(Subsystem, metaclass=Singleton):
    """
        Below fields are assigned only for the IDE to identify that they are values
    """
    def __init__(self):
        super().__init__()
        self.configuration: str | FilePath | None
        self.persistence_base: str | DirectoryPath | None
        self.certificate_base: str | DirectoryPath | None
        self.client_certificate: str | FilePath | None
        self.client_key: str | FilePath | None
        self.server_certificate: str | FilePath | None
        self.server_key: str | FilePath | None
        self.datastore: str | FilePath | None
        self.api_listen_host: str | IPvAnyAddress | None
        self.api_listen_port: conint(gt=0, le=65535) | None
        self.elevenlabs_api_key: str | None
        self.openai_api_key: str | None

    def bootstrap(self):
        """ Bootstrap for Configuration
        check if a value is returned from `find_configuration_path`, if it isn't, the path doesn't exist.
        we need to call `first_run` so that a valid configuration file exists to load.
        `load_configuration` is called to read in the config and inherit the data to the Subsystem.
        set the active flag to indicate we are ready from processing and start the worker to process from the queue.
        """
        if not self.find_configuration_path():
            self.first_run()
        elif not os.path.exists(self.find_configuration_path()):
            self.first_run()
        self.load_configuration()
        self.active = True
        self.worker.start()

    def first_run(self):
        """ Called when the configuration data isn't found on disk, implying this is the first run of the subsystem.
            Create a default ServerConfiguration and change the configuration path to be where the configuration will
            exist (in the case that it's set to a non-default value or inherited from env vars).
            Note: the file needs to exist to satisfy the Filepath validator for ServerConfiguration, so we write an
                  empty dict to the file initially.
            finally, write the configuration data to disk.
        """
        # todo create the files that will be missing.
        configuration = ServerConfiguration()

        with open(self.find_configuration_path(), 'w') as conffd:
            conffd.write(configuration.json())
        self.inherit_data(configuration)

    def inherit_data(self, model: ServerConfiguration):
        """ Combine the values from the ServerConfiguration with the Subsystem instance."""
        with self.lock.w_locked():
            logging.info('Inheriting data from ServerConfiguration...')
            for k, v in model.dict().items():
                try:
                    logging.debug(f'New Configuration CVAR: {k} {v}')
                except Exception as e:
                    logging.error(f'Error displaying new CVAR in logfile: {e}')
                self.__dict__[k] = v

    @staticmethod
    def write_configuration(model: ServerConfiguration):
        """ Write configuration to disk. """
        with open(model.configuration, 'w') as conffd:
            conffd.write(model.json(indent=4))
        logging.info(f'Wrote {str(model.configuration)}')

    def find_configuration_path(self):
        f""" Check operational vars to determine where the configuration data is.
            Confirm it exists and return it.
            If the env flag "{about.__TITLE__}_CONFPATH" is set then overwrite the self.configuration value to represent
            it's location. The bootstrap should ensure the other values are correctly loaded from the configuration file
            supplied.
         """
        if f"{about.__TITLE__}_CONFPATH" in os.environ:
            assert os.path.exists(os.environ[f"{about.__TITLE__}_CONFPATH"])
            logging.info(f'Using environment variable for configuration: {os.environ[f"{about.__TITLE__}_CONFPATH"]}')
            with self.lock.w_locked():
                self.configuration = os.environ[f"{about.__TITLE__}_CONFPATH"]
            return os.environ[f"{about.__TITLE__}_CONFPATH"]
        else:
            with self.lock.w_locked():
                self.configuration = os.path.join('worldgpt', 'server',
                                                  'persistence', 'configuration', 'configuration.json')

        return self.configuration

    def load_configuration(self):
        """ Load the values from the configuration file into to the Configuration Subsystem. """
        with open(self.configuration, 'r') as conffd:
            data = dict(json.loads(conffd.read()))
            configuration = ServerConfiguration(**data)
        self.inherit_data(configuration)
