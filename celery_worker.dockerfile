FROM python:3-slim

WORKDIR /app

COPY ["requirements.txt", "/app/"]

RUN pip install $(cat requirements.txt | grep -E "celery|redis")

# for debug
RUN pip install debugpy

COPY ["app/tasks/celery_worker.py", "/app/tasks/"]

CMD ["celery", "-A", "tasks.celery_worker.celery", "worker", "--loglevel=DEBUG"]