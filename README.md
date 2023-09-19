# Building Queue with FastAPI, Celery, Redis and Flower 


To start everything run: 

```bash
docker compose -f docker-compose.yaml up  
```

Then run the FastAPI app locally with your env end your favorite tool. 

## Overview

- **Timescale DB** (postgres) backend 
- **Rediis** as broker

- **Celery workers** as Queues. There are three workers (i.e. three queues).
  1. High prio fast running tasks 
  2. Low prio slow running tasks 
  3. Periodically running tasks with beat worker

- **Fast API** as webapp (not part of the docker compose)

- **Flower** for monitoring the running tasks
There is flower running for monitoring the different tasks that are running. 
The idea would be here that we can monitor this as well with grafana.
On http://localhost:5555/ you find an overview on all task that are running. 


