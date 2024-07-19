FROM python:3.11

ENV PYTHONUNDUFFERED=1

WORKDIR /var/weather_app

RUN pip install --upgrade pip "poetry==1.8.3"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY weather_app .

CMD ["weather_app.wsgi:application", "--bind", "0.0.0.0:8000"]