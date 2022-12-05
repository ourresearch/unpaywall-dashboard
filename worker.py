from app import rq

# Creates a worker that handle jobs in ``default`` queue.
default_worker = rq.get_worker()
default_worker.work()
