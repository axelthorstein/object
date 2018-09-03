FROM python:3.6.6-slim-jessie

# -- Install Pipenv.
RUN pip install pipenv

# -- Set the working directory.
WORKDIR /app

# -- Adding Pipfiles.
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install Python dependencies.
RUN set -ex && pipenv install --system

# -- Install system dependencies.
RUN apt-get update && apt-get install -y libsm6 libxext6 libgtk2.0 tk

# -- Copy project into working directory.
COPY . /app

CMD ["gunicorn", "--config", "gunicorn.conf.py", "--log-level", "info", "main:app"]
