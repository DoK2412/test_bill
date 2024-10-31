FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --root-user-action=ignore

COPY ./ /code/

CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8084"]