# Copyright (c) 2017 "Shopify inc." All rights reserved.
# Use of this source code is governed by a MIT-style license that can be found in the LICENSE file.
python_files := find . -path '*/.*' -prune -o -name '*.py' -print0
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))

all: test

clean:
	find . \( -name '*.pyc' -o -name '*.pyo' -o -name '*~' \) -print -delete >/dev/null
	find . -name '__pycache__' -exec rm -rvf '{}' + >/dev/null
	pipenv clean

autoformat:
	yapf --in-place --recursive --style google .

lint:
	@pylint -j 4 --rcfile=pylintrc obj/*.py tests/*.py configs/*.py utils/*.py *.py 

autolint: autoformat lint

run_test: clean
	pytest .

test: autolint run_test lint

install:
	pipenv install

shell:
	pipenv shell
