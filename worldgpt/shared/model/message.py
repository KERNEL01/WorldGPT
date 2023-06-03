import datetime
from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    """ A message object for use in issuing information to the language model. """
    role: Literal['user', 'system', 'assistant']  # openai specific
    content: str
    timestamp: float = float(datetime.datetime.now().timestamp())

    def to_openai(self, preserve_timestamp=False):
        """ Return a dictionary that can be used with OpenAI api calls. Timestamp is used only by WorldGPT. """
        message = self.dict()
        if preserve_timestamp:
            time_str = datetime.datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            message['content'] = f"{time_str}: {self.content}"
        message.pop("timestamp")
        return message
