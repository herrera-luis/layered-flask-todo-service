FROM python:3.9.12-alpine 

RUN apk update && apk add musl-dev libpq-dev gcc

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt 

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

EXPOSE 5000

CMD ["python", "run.py"]