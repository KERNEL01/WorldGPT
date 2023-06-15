

"""
    API
    ===

    The API is a work in progress. It's still subject to change and isn't yet ready.
    I'd like feedback on the API, as I think that my opinion on how it should be constructed is probably not the best
    way to do it.

    The API is designed to be a RESTful API, with the following endpoints:

"""


import os
from typing import Literal, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from worldgpt.shared.model.character import Character
from worldgpt.shared.model.message import Message
from worldgpt.shared.util import about


application = FastAPI()


origins = [
    'http://localhost:8001',
    'http://localhost:63342'
           ]


application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@application.get("/")
def root():
    return {"title": about.__TITLE__,
            "tag": about.__STATUS__,
            "version": about.__VERSION__,
            "author": about.__AUTHOR__}


@application.get("/characters")
def get_characters():
    """ Returns a list of all characters."""
    from worldgpt.server.subsystem.database import Database
    output = {}
    with Database().lock.r_locked():
        characters = dict(Database().characters)
    for character in characters:
        output[character] = characters[character].dict()
    return output


@application.post('/characters/new')
def create_character(character: Character):
    """ Creates a new character."""
    from worldgpt.server.subsystem.database import Database
    with Database().lock.r_locked():
        characters = dict(Database().characters)
    if character.name in characters:
        return {'error': 'Character already exists.'}
    Database().queue.put(character)
    return {'success': 'Character created.'}


@application.delete('/characters/{name}')
def delete_character(name: str):
    """ Deletes a character."""
    from worldgpt.server.subsystem.database import Database
    with Database().lock.r_locked():
        characters = dict(Database().characters)
    if name not in characters:
        return {'error': 'Character does not exist.'}
    # todo deletion request to queue. return {'success': 'Character deleted.'}
    return {'error': 'Not implemented.'}


@application.get('/characters/prompts/{name}')
def get_character_prompts(name: str):
    """ Returns a list of all prompts for a character."""
    from worldgpt.server.subsystem.database import Database
    with Database().lock.r_locked():
        characters = dict(Database().characters)
    if name not in characters:
        return {'error': 'Character does not exist.'}
    messages = characters[name].to_prompt_messages()
    output = []
    for message in messages:
        output.append(message.json())
    return output


@application.post('/generate/openai/llm_completion')
def generate_llm_completion(character: str,
                            messages: List[Message],
                            model: Literal['gpt-3.5-turbo'] = 'gpt-3.5-turbo'):
    """ Generates a completion from a message using the LLM model."""
    from worldgpt.server.subsystem.database import Database
    with Database().lock.r_locked():
        characters = dict(Database().characters)
    if character not in characters:
        return {'error': 'Character does not exist.'}
    for message in messages:
        if message.content == '':
            return {'error': 'Message is empty.'}
        if len(message.content) > 2048:
            return {'error': 'Message is too long.'}
    from worldgpt.server.util.llm import generate_chat_completion
    resp = generate_chat_completion(characters[character], external_messages=messages, model=model)
    return {'completion': resp.json()}


def run_in_main_thread():
    import uvicorn
    from worldgpt.server.subsystem.configuration import Configuration
    with Configuration().lock.r_locked():
        api_listen_host = Configuration().api_listen_host or "127.0.0.1"
        api_listen_port = Configuration().api_listen_port or 8000
    uvicorn.run('worldgpt.server.subsystem.api:application',
                host=os.environ.get('wgpt_listen_address', api_listen_host),
                port=os.environ.get('wgpt_listen_port', api_listen_port),
                )
