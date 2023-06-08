#!/bin/sh

docker-compose run test pytest -v -p no:warnings
