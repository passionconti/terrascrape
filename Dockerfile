FROM python:3.7-slim AS base

# set the language
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

## pip install
RUN pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install --no-cache-dir --upgrade pip setuptools wheel

# set terrascrape files
ENV TERRASCRAPE_PATH=/usr/local/terrascrape
COPY requirements.txt ${TERRASCRAPE_PATH}/requirements.txt
RUN pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r ${TERRASCRAPE_PATH}/requirements.txt

ENV PYTHONPATH ${TERRASCRAPE_PATH}
WORKDIR ${TERRASCRAPE_PATH}

COPY terrascrape ${TERRASCRAPE_PATH}/terrascrape

CMD ["python", "terrascrape/cli/__init__.py", "webserver"]

FROM base AS test

COPY tests ${TERRASCRAPE_PATH}/tests
