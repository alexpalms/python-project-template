FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv venv
RUN uv pip install -e . --group dev

CMD ["/bin/bash", "docker/entrypoint.sh"]