FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY bioagents ./bioagents
COPY demos ./demos

RUN pip install --no-cache-dir .

CMD ["bioagents", "run", "demos/sample_task.json"]
