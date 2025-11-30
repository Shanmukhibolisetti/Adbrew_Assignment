FROM python:3.10

WORKDIR /src/rest
ENV ENV_TYPE staging
ENV MONGO_HOST mongo
ENV MONGO_PORT 27017
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ .

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --run-syncdb && python manage.py runserver 0.0.0.0:8000"]
