

"""
    API
    ===

    The API is a work in progress. It's still subject to change and isn't yet ready.
    I'd like feedback on the API, as I think that my opinion on how it should be constructed is probably not the best
    way to do it.

    The API is designed to be a RESTful API, with the following endpoints:

"""


import os
from fastapi import FastAPI

from worldgpt.shared.model.character import Character
from worldgpt.shared.util import about


application = FastAPI()


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


def run_in_main_thread():
    import uvicorn
    from worldgpt.server.subsystem.configuration import Configuration
    with Configuration().lock.r_locked():
        api_listen_host = Configuration().api_listen_host or "127.0.0.1"
        api_listen_port = Configuration().api_listen_port or 8000
    uvicorn.run('worldgpt.server.subsystem.api:application',
                host=os.environ.get('wgpt_listen_address', api_listen_host),
                port=os.environ.get('wgpt_listen_port', api_listen_port),
                reload=True
                )
