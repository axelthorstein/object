FROM python:3.6.6-jessie

# LABEL python_version=python3.6
# RUN virtualenv --no-download /env -p python3.6

# -- Install Pipenv.
RUN pip install pipenv

# -- Set the working directory.
WORKDIR /app

# -- Adding Pipfiles.
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies.
RUN set -ex && pipenv --python 3.6.6 && pipenv install

# -- Copy project into working directory.
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
