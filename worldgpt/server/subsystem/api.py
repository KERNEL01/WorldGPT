

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
from worldgpt.shared.util import about


application = FastAPI()


@application.get("/")
def root():
    return {"title": about.__TITLE__,
            "tag": about.__STATUS__,
            "version": about.__VERSION__,
            "author": about.__AUTHOR__}


def run_in_main_thread():
    import uvicorn
    uvicorn.run(application,
                host=os.environ.get('wgpt_listen_address', '127.0.0.1'),
                port=os.environ.get('wgpt_listen_port', 8000)
                )
