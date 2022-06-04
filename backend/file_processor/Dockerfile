FROM python:3.10

RUN pip install poetry==1.1.13

WORKDIR /file_processor
COPY ./pyproject.toml /file_processor/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . .

CMD ["bash", "./run_service.sh"]
