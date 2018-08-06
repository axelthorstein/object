FROM python:3.6.6-jessie

# LABEL python_version=python3.6
# RUN virtualenv --no-download /env -p python3.6

# -- Install Pipenv:
RUN apt update && apt install python3-pip git -y && pip3 install pipenv

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Application into container:
RUN set -ex

WORKDIR /app

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv --python 3.6.6 && pipenv install

# -- Copy project:
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
