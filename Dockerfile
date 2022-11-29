FROM python:3.10
WORKDIR /app
RUN pip3 install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry install -n
COPY . /app
EXPOSE 8000
CMD poetry run sanic --port=8000 --host=0.0.0.0 load_balancer.app:app