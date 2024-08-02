FROM python:3-slim

WORKDIR /app

ENV CELERY_RDBSIG=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV C_FORCE_ROOT=1
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

RUN pip install $(cat requirements.txt | grep -E "celery|redis")

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["celery", "-A", "app.worker.celery", "worker", "--loglevel=INFO", "--concurrency=1", "--pool=solo"]