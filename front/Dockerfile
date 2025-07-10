FROM node:18-alpine AS builder


WORKDIR /app
COPY ./app/package*.json ./
RUN npm ci
COPY ./app .

EXPOSE 5173
ENTRYPOINT ["npm", "run", "build"]

