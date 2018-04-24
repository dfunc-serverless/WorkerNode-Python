from worker_node import WorkerPool


if __name__ == "__main__":
    worker_pool = WorkerPool()
    try:
        worker_pool.start()
    except KeyboardInterrupt:
        worker_pool.kill()
