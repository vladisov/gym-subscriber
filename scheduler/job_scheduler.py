from concurrent.futures import ProcessPoolExecutor

import redis

from model.job_model import Job


class JobScheduler:

    def __init__(self, number_of_jobs):
        self.executor = ProcessPoolExecutor(number_of_jobs)
        self.job_map = {}
        self.redis = redis.Redis()

    def add_job(self, job):
        # redis?
        future = self.executor.submit(job.job_process)
        self.job_map[job.job_id] = Job(job.job_id, "RUNNING")
        job_dict = self.job_map[job.job_id]
        self.redis.set(job.job_id, "RUNNING")
        # future.add_done_callback(functools.partial(self._finish_job, job.job_id))

    def cancel_job(self, job_id):
        status = self.redis.get(job_id)
        if status is not None and status.decode('utf-8') == 'RUNNING':
            self.redis.set(job_id, "CANCELLED")

    def _finish_job(self, job_id):
        self.job_map[job_id].pop()

    def get_jobs(self):
        return self.job_map

    def get_job_state(self, job_id):
        if job_id in self.job_map:
            return self.job_map[job_id]
