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
COPY ./Dockerfile /app/Dockerfile
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock
COPY ./configs /app/configs
COPY ./gunicorn.conf.py /app/gunicorn.conf.py
COPY ./heroku.yml /app/heroku.yml
COPY ./image_filters /app/image_filters
COPY ./images /app/images
COPY ./main.py /app/main.py
COPY ./manifest.json /app/manifest.json
COPY ./object /app/object
COPY ./static /app/static
COPY ./templates /app/templates
COPY ./utils /app/utils

CMD ["gunicorn", "--config", "gunicorn.conf.py", "--log-level", "info", "main:app"]
