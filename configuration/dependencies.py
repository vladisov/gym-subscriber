from flask_injector import request

from repository.repository import Repository


def configure(binder):
    binder.bind(Repository, to=Repository, scope=request)
