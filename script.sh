#!/bin/bash

# Set timezone to make run cron based on GMT+9.
TZ="Asia/Seoul"
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

DATE=$(date "+%Y-%m-%d_%H%M")
TEST_RES=$(speedtest --format=json-pretty --accept-license)

tocuh /logs/${DATE}_networktest.json && chmod 0644 /logs/${DATE}_networktest.json 2>&1
echo ${TEST_RES} > /logs/${DATE}_networktest.json 2>&1