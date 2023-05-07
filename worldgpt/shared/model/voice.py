

from typing import Literal, Union, List
from pydantic import BaseModel, FilePath, conlist


class Voice(BaseModel):
    """
        Voice dataclass.
            Stores information for generation of voice messages.

        name
            elevenlabs: should link back to the name of the voice.
        samples
            training data for voice model, ideally pointing to stored data on disk
        description:
            elevenlabs: used for generation of voice model.
            a description or flair used to describe the voice.
        accent:
            elevenlabs: honestly, barely works. pls fix this Elevenlabs.
        language:
            elevenlabs: support to multiple languages.
        filler_messages:
            these are meant to be messages to stream back to the client when things take too long, it gives the user an
            audible indication that it's still processing.
    """

    name: str
    samples: conlist(Union[bytes, FilePath], max_items=25, unique_items=True)
    description: str
    accent: str
    language: str
    gender: Literal['Male', 'Female', 'Non-Binary']
    filler_messages: List[FilePath]
