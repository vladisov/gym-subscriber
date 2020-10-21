import uuid

from flask import Flask
from flask import jsonify
from flask import request
from flask_injector import FlaskInjector
from injector import inject

from configuration.dependencies import configure
from model.job_model import JobRequest
from repository.repository import Repository
from scheduler.job_scheduler import JobScheduler
from service.subscribe_service import SubscribeTask

flask_app = Flask("gym-sub")


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
@flask_app.route('/submit')
def submit_job(scheduler: JobScheduler):
    class_id = request.args.get('class_id')
    job_id = str(uuid.uuid1())
    subscribe_service = SubscribeTask(job_id, class_id)
    scheduler.add_job(JobRequest(job_id, subscribe_service))
    return f'Created job with job id - {job_id}'


@inject
@flask_app.route('/cancel')
def cancel_job(scheduler: JobScheduler):
    job_id = request.args.get('job_id')
    scheduler.cancel_job(job_id)
    return f'Job has been canceled - {job_id}'


@inject
@flask_app.route('/info')
def get_info(scheduler: JobScheduler):
    # job_id = request.args.get('id')
    jobs = scheduler.get_jobs()
    return jsonify(jobs)
    # if job_id in jobs:
    #     return jsonify(scheduler.get_jobs()[job_id].done())
    # return jsonify(f'job with id = {job_id} has not been found')


FlaskInjector(app=flask_app, modules=[configure])
