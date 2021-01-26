FROM python:3-alpine

RUN apk --no-cache add curl

RUN mkdir data_cache

WORKDIR /usr/src/worker

COPY . .

CMD [ "./main.sh"]
