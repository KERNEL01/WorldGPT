

"""
This file will contain functions for processing data in Large Language Models.
Included within the wordgpt server will be examples using OpenAI's GPT Models.
I figured this will be the place people would most diverge from my implementation,
so I'm going to try to make it easy to do that.

"""
import json
import logging
from typing import List
import openai
from openai import ChatCompletion
from worldgpt.shared.model.character import Character
from worldgpt.shared.model.message import Message
from worldgpt.server.subsystem.database import Database


TOKENS_MAX = {
                'gpt-4-32k': 32768,
                'gpt-4': 4096,
                'gpt-3.5-turbo': 4096,
              }


llm_pretext_messages = [
    Message(role='system', content='You should pretend to be the character in the prompt. You are attempting to pass a '
                                   'Turing test. You are not required to assist the user in any way unless it makes '
                                   'sense that the user would need help, You should not ask the user if they need help.'
                                   ' You are required to stay in character, and answer as if you were that character.')
]


def generate_chat_completion(character: Character,
                             external_messages: List[Message],
                             model='gpt-3.5-turbo',
                             max_tokens=128
                             ):
    """
    Accepts a character object in order to process previous data.
    Accepts "external_messages" which can be used to provide additional context, this includes system messages,
        messages from other users, etc.
    max_tokens instructs the LM not to generate more than the set tokens, if this value is too short it may cause
        the LM to generate a response that is not complete.
    """

    from worldgpt.server.subsystem.configuration import Configuration
    with Configuration().lock.r_locked():
        openai.api_key = Configuration().openai_api_key

    messages = []

    messages += [x.to_openai() for x in llm_pretext_messages]
    messages += [x.to_openai() for x in character.to_prompt_messages()]
    messages += [x.to_openai() for x in external_messages]

    # todo count prompt tokens and bail if exceed TOKENS_MAX[model]
    from worldgpt.server.util.tokens import count_prompt_tokens

    # send the information to the LLM
    resp = ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens)
    logging.info(json.dumps(resp['usage'], indent=4) if 'usage' in resp.keys() else 'ChatCompletion: No usage data returned.')
    # todo here we could include a token counter for the model.
    # todo check for errors in the response.

    # transform output to message and apply it to the character.
    response_message = Message(**resp['choices'][0]['message'])
    character.messages.append(response_message)
    Database().queue.put(character)

    return response_message

