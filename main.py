from worker_node import WorkerPool, WorkerThread


if __name__ == "__main__":
    # worker_pool = WorkerPool()
    # try:
    #     worker_pool.start()
    # except KeyboardInterrupt:
    #     worker_pool.kill()
    worker = WorkerThread(0)
    worker.start()
