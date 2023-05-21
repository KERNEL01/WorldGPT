

import os
from pydantic import BaseModel, DirectoryPath, FilePath


class Configuration(BaseModel):
    persistence_base: DirectoryPath
    client_certificate: FilePath
    client_key: FilePath
    datastore: FilePath
