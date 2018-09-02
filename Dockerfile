FROM python:3.6.6-alpine

RUN pip install --upgrade pip

RUN pip3 install opencv-python==3.4.2.17

# -- Install Pipenv.
RUN pip install pipenv

# -- Set the working directory.
WORKDIR /app

# -- Fix opencv-python issue.
RUN apk add gcc g++ libpng freetype-dev
# libsm6 libxext6 

# -- Adding Pipfiles.
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies.
RUN set -ex && pipenv install --system

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
