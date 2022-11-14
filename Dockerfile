FROM python:3.9
WORKDIR /scuffed-kv
COPY ./requirements.txt /scuffed-kv/requirements.txt
COPY ./db /scuffed-kv/db/
RUN pip install --no-cache-dir --upgrade -r /scuffed-kv/requirements.txt
COPY ./app /scuffed-kv/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]