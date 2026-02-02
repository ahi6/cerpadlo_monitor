# syntax=docker/dockerfile:1

FROM alpine:3.23
WORKDIR /cerpadlo
COPY . .

RUN apk add python3 py3-pip py3-lxml py3-requests
RUN pip install --break-system-packages influxdb-client==1.50.0

CMD ["watch", "-n", "180", "python3", "scrape_everything.py"]