#!/bin/bash

# docker compose up --build

#poetry run ./backend/run.sh

bash -c "cd ./backend/ && poetry run ./run.sh > /dev/null 2>&1 &"
 
bash -c "cd ./front/app/ && npm run dev > /dev/null 2>&1 &"

echo "Процесс запущен"
