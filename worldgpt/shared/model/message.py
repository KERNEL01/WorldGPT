

from pydantic import BaseModel


class Message(BaseModel):
    """ A message object for use in issuing information to the language model. """
    role: str
    content: str
