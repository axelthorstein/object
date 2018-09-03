FROM python:3.6.6-jessie

# -- Install Pipenv.
RUN pip install pipenv

# -- Set the working directory.
WORKDIR /app

# -- Adding Pipfiles.
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies.
RUN set -ex && pipenv install --system

# -- Fix opencv-python issue.
RUN apt-get install -y libsm6 libxext6

# -- Copy project into working directory.
COPY . /app

CMD ["gunicorn", "--config", "gunicorn.conf.py", "--log-level", "info", "main:app"]
