from celery import Celery
from celery import current_app
from flask import Flask
from flask import jsonify
from flask import request
from flask_injector import FlaskInjector
from injector import inject

from configuration.dependencies import configure
from repository.repository import Repository


def init_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['BACKEND'],
        broker=app.config['BROKER']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


_ = current_app.loader.import_default_modules()

flask_app = Flask("gym-sub")
flask_app.config.update(
    BROKER='redis://localhost:6379',
    BACKEND='redis://localhost:6379'
)

celery = init_celery(flask_app)


@inject
@flask_app.route('/')
def get_week_info(repo: Repository):
    week = request.args.get('week')
    activity = request.args.get('activity')
    weekInfo = repo.find_all(week_start=week, activity_type=activity)
    if weekInfo is None:
        return "Not found"
    return jsonify(weekInfo)


@inject
@flask_app.route('/add')
def add(repo: Repository):
    result = add_together.delay(5, 7)
    return result.wait()


@flask_app.route('/get_all')
def get_all():
    tasks = list(sorted(name for name in current_app.tasks
                        if not name.startswith('celery.')))
    return jsonify(tasks)


@celery.task()
def add_together(a, b):
    """executing"""
    return a + b


FlaskInjector(app=flask_app, modules=[configure])
