all: clean install test

clean:
	find . \( -name '*.pyc' -o -name '*.pyo' -o -name '*~' \) -print -delete >/dev/null
	find . -name '__pycache__' -exec rm -rvf '{}' + >/dev/null
	pipenv clean

autoformat:
	yapf --in-place --recursive --style google .

lint:
	@pylint -j 4 --rcfile=pylintrc object/*.py tests/*.py configs/*.py utils/*.py *.py 

autolint: autoformat lint

run_test: clean
	pytest .

test: autolint run_test lint

install:
	pipenv install

shell:
	pipenv shell
