

import os
from pydantic import DirectoryPath, FilePath, conint
from worldgpt.shared.model.configuration import Configuration
from pydantic.networks import IPvAnyAddress


class ServerConfiguration(Configuration):

    persistence_base: DirectoryPath = os.path.join('worldgpt', 'server', 'persistence')

    client_certificate: FilePath = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'client.crt.pem')
    client_key: FilePath = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'client.key.pem')

    server_certificate: FilePath = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'server.crt.pem')
    server_key: FilePath = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'server.key.pem')

    datastore: FilePath = os.path.join('worldgpt', 'server', 'persistence', 'database', 'datastore.db')
    configuration: FilePath = os.path.join('worldgpt', 'server', 'persistence', 'configuration', 'configuration.json')

    api_listen_host: str | IPvAnyAddress = "localhost"
    api_listen_port: conint(gt=0, le=65535) = 8001

    elevenlabs_api_key: str = ""
    openai_api_key: str = ""
