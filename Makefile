all: clean install test

clean:
	@echo 'Removing extra Python files and unused dependencies.'
	@find . \( -name '*.pyc' -o -name '*.pyo' -o -name '*~' \) -print -delete >/dev/null
	@find . -name '__pycache__' -exec rm -rvf '{}' + >/dev/null
	@pipenv clean

format:
	@echo 'Formatting code in place according to Yapf.'
	@yapf --in-place --recursive --style google .

lint:
	@echo 'Linting code.'
	@pylint -j 4 --rcfile=pylintrc object/*.py tests/*.py configs/*.py utils/*.py *.py 

autolint: format lint

run_test: clean
	@echo 'Running test cases.'
	@pytest .

test: autolint lint run_test

install:
	@pipenv install

shell:
	@pipenv shell

server:
	@python main.py

docker: clean
	@docker build . -t object_test && docker run -it -p 8080:8080 object_test
