

from pydantic import BaseModel
from pydantic.types import Path


class Configuration(BaseModel):
    persistence_base: Path
    client_certificate: Path
    client_key: Path
    datastore: Path