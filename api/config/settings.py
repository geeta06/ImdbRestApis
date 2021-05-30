'''This is setting file for project to write configuration'''

import os
import logging


class Config(object):
    """
    Configuration class for Project.
    """

    SECRET_KEY = '5f0acecb54c04779bf8e348898b6c382'
    LOG_CONFIGURATION = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }