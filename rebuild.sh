#!/bin/sh

docker-compose -f docker-compose.yml down

docker image rm -f terrascrape_terrascrape
docker image rm -f terrascrape_test

docker-compose -f docker-compose.yml up -d
