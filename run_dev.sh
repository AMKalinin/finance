#!/bin/bash


docker-compose -f dev.docker-compose.yaml up

bash -c "cd ./backend/ && poetry run ./run.dev.sh > /dev/null 2>&1 &"
 
bash -c "cd ./front/app/ && npm run dev > /dev/null 2>&1 &"

echo "Процесс запущен"
