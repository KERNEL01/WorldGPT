

import json
from datetime import datetime
from typing import Optional, Literal, List
from pydantic import BaseModel, Field
from worldgpt.shared.model.message import Message


class Character(BaseModel):
    """ A character dataclass
    a note on tokens:
        You can make a less-informed guess on the token count according to:
                1 token ~= 4 chars in English
                1 token ~= ¾ words
                100 tokens ~= 75 words
        this is not a hard and fast rule, but it is a good rule of thumb. This is only important on choosing whether
        you can supply all previous communiqué with a prompt to the LM API, or if you need to supply only the summaries
        to prevent limiting the response generation.

        with openai + plus subscription it gives you the ability to utilise 8K tokens, which includes both the prompt
        and the response to the prompt.
    a note on summaries:
        Summaries are generated by the LM API, and are used to reduce the token count of the prompt. This is done by
        feeding the previous messages to the LM API and asking it to summarise important information from the
        conversation. This is useful for reducing the token count of the prompt, but it is not perfect.
        It does provide a way for users to simulate "memory", as it will invariably summarise down and lose some
        information. This could mean that critical information from a conversation isn't captured in the summary,
        but it's a limitation I can't really get around.
    """
    name: str = Field(description="The full name of the character")
    description: str = Field(description="A physical description of the character, "
                                         "not necessarily what they are wearing or doing.")
    rank: Optional[str] = Field(description="The rank or renown of a character.")
    title: Optional[str] = Field(description="Any titles the character has. Typically MR or MRS, DR, etc.")
    occupation: Optional[str] = Field(description="The occupation of the character.")
    age: Optional[float] = Field(description="The age of the character, represented as a float.")
    birthdate: Optional[float] = Field(description="The birthdate of the character, represented as a float, "
                                                   "when sent to the model, "
                                                   "it will be converted to a human readable datetime.")
    gender: Literal["Male", "Female", "Non-Binary"]
    alignment: Optional[Literal["Lawful-Good", "Neutral-Good", "Chaotic-Good",
                                 "Lawful-Neutral", "True-Neutral", "Chaotic-Neutral",
                                 "Lawful-Evil", "Neutral-Evil", "Chaotic-Evil"]]
    mood: Optional[str] = Field(description="Helps the model determine how to interact with the player. ")
    attributes: Optional[List[str]] = Field(description="A list of psychological or physical attributes "
                                                        "that the character has.Ex : [\"brave\", \"strong\"].")

    health: Optional[float] = Field(description="The health of the character, represented as a float.")
    inventory: Optional[List[str]] = Field(description="A list of items the character has. Ex: [\"sword\", \"shield\"]")

    messages: List["Message"] = Field(description="A list of messages that has been generated by the player or the LM.")
    summaries: List[str] = Field(description="A list of summaries that has been generated by the LM based on Messages. "
                                             "These are integral to reducing Token amounts when submitting to LM APIs.")

    meta: List["Message"] = Field(description="A list of messages that is considered meta information. This should be"
                                              "considered as a method of provided extra information to the LM that is"
                                              "*specific* to the character. ie. a rule that the character may have.")

    @staticmethod
    def sql_schema():
        return f""""CREATE TABLE IF NOT EXISTS Character(
                    name varchar primary key not null,
                    description varchar not null,
                    rank varchar,
                    title varchar,
                    occupation varchar,
                    age float,
                    birthdate float,
                    gender varchar not null,
                    mood varchar,
                    attributes varchar,
                    health float,
                    inventory varchar,
                    messages varchar not null,
                    summaries varchar not null
                );"""

    def to_sql(self):
        query = f"""INSERT OR REPLACE INTO Character( {', '.join(self.__fields__.keys())} ) VALUES ({"?," * (len(self.__fields__.keys()) - 1)}?);"""
        return query, [self.name,
                       self.description,
                       self.rank,
                       self.title,
                       self.occupation,
                       self.age,
                       self.birthdate,
                       self.gender,
                       self.alignment,
                       self.mood,
                       json.dumps(self.attributes),
                       self.health,
                       json.dumps(self.inventory),
                       json.dumps([x.dict() for x in self.messages]),
                       json.dumps(self.summaries),
                       json.dumps([x.dict() for x in self.meta])
                       ]

    def to_prompt_messages(self):
        """ Convert character information into Message objects that can be used as prompts for the LM. """
        prompts = []
        messages = []
        prompts.append(f"Your name is {self.name}")
        prompts.append(f"You can be described as: {self.description}")
        prompts.append(f"You are {self.gender}")
        if self.alignment:
            prompts.append(f"Your alignment is {self.alignment}")
        # todo health to prompt
        if self.health:
            prompts.append(f"You have {self.health} health")
        if self.mood:
            prompts.append(f"You are feeling {self.mood}")
        if self.rank:
            prompts.append(f"You are the rank of {self.rank}")
        if self.title:
            prompts.append(f"You title is {self.title}")
        if self.occupation:
            prompts.append(f"You work as a {self.occupation}")
        if self.age:
            age = datetime.fromtimestamp(self.age)
            repr_age = f"{age.year} years, and {age.month} months"
            prompts.append(f"You are {repr_age} old")
        if self.birthdate:
            bd = datetime.fromtimestamp(self.birthdate)
            repr_bd = f"{bd.month}, {bd.day}"
            prompts.append(f"Your birthday is {repr_bd}")
        if self.attributes:
            prompts.append(f"you have the following attributes: {', '.join(self.attributes)}")
        if self.inventory:
            prompts.append(f"You have the following items: {', '.join(self.inventory)}")

        for prompt in prompts:
            messages.append(Message(role="system", content=prompt))
        for message in self.messages:
            messages.append(messages)
        # todo decide if we're checking for prompt size here, or we're doing it further in the process.
        # todo wearing clothing instead of having it as an item.
        return messages
