


import os
from pydantic.types import Path
from pydantic import conint
from worldgpt.shared.model.configuration import Configuration
from pydantic.networks import IPvAnyAddress


class ServerConfiguration(Configuration):

    persistence_base: Path = os.path.join('worldgpt', 'server', 'persistence')

    client_certificate: Path = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'client.crt.pem')
    client_key: Path = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'client.key.pem')

    server_certificate: Path = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'server.crt.pem')
    server_key: Path = os.path.join('worldgpt', 'server', 'persistence', 'certificate', 'server.key.pem')

    datastore: Path = os.path.join('worldgpt', 'server', 'persistence', 'database', 'datastore.db')
    configuration: Path = os.path.join('worldgpt', 'server', 'persistence', 'configuration', 'configuration.json')

    api_listen_host: str | IPvAnyAddress = "localhost"
    api_listen_port: conint(gt=0, le=65535) = 8001

    elevenlabs_api_key: str = ""
    openai_api_key: str = ""