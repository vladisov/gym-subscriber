from injector import singleton

from repository.repository import Repository
from scheduler.job_scheduler import JobScheduler


def configure(binder):
    binder.bind(Repository, to=Repository, scope=singleton)
    binder.bind(JobScheduler, to=JobScheduler(4), scope=singleton)
