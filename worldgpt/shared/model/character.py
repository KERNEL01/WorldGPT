import json
from typing import Optional, Literal, List
from pydantic import BaseModel
from worldgpt.shared.model.message import Message


class Character(BaseModel):
    """ A character dataclass
            Stores information relating to the character, that can be used to enrich the language model's generation.

        Summaries
            To reduce token size, the summaries field summarises a previous conversation to parts of the conversation
            that the language model deems important.
    """

    name: str
    description: str
    rank: Optional[str]
    title: Optional[str]
    occupation: Optional[str]
    age: Optional[float]
    gender: Literal["Male", "Female", "Non-Binary"]

    mood: Optional[str]
    attributes: Optional[List[str]]

    health: Optional[float]
    inventory: List[str]

    messages: List[Message]
    summaries: List[str]

    @staticmethod
    def sql_schema():
        return f""""CREATE TABLE IF NOT EXISTS Character(
                    name varchar primary key not null,
                    description varchar not null,
                    rank varchar,
                    title varchar,
                    occupation varchar,
                    age float,
                    gender varchar not null,
                    mood varchar,
                    attributes varchar,
                    health float,
                    inventory varchar,
                    messages varchar not null,
                    summaries varchar not null
                );"""

    def to_sql(self):

        query = f"""INSERT OR REPLACE INTO Character( {', '.join(self.__fields__.keys())} ) VALUES ({"?," * (len(self.__fields__.keys()) -1)}?);"""
        fields = [json.dumps(x) for x in self.__fields__.values()]
        return query, [self.name,
                       self.description,
                       self.rank,
                       self.title,
                       self.occupation,
                       self.age,
                       self.gender,
                       self.mood,
                       json.dumps(self.attributes),
                       self.health,
                       json.dumps(self.inventory),
                       json.dumps([x.dict() for x in self.messages]),
                       json.dumps(self.summaries)
                       ]