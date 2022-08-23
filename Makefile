# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* customerclustering-frontend/*.py

black:
	@black scripts/* customerclustering-frontend/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr customerclustering-frontend-*.dist-info
	@rm -fr customerclustering-frontend.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)


streamlit_run:
	streamlit run app.py

### DOCKER 
# Build an image whenever the model changes
build_docker_image:
	docker build --tag asia.gcr.io/wagon-le-8888/customerclustering-frontend . 

docker_run:
	docker run -e PORT=8002 -p 3000:8002 asia.gcr.io/wagon-le-8888/customerclustering-frontend

# Hop inside my shell
docker_interactive:
	docker run -e PORT=8001 -p 3000:8001 -it asia.gcr.io/wagon-le-8888/customerclustering-frontend sh