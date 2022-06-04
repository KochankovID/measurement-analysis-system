FROM python:3.10

RUN pip install poetry==1.1.13

WORKDIR /measurement_gateway
COPY ./pyproject.toml /measurement_gateway/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . .

CMD ["bash", "./scripts/fastApi-entrypoint.sh"]
