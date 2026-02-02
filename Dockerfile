# syntax=docker/dockerfile:1

FROM python:alpine3.22
WORKDIR /cerpadlo
COPY . .

# needed for lxml dependencies
RUN apk add libxml2 libxslt gcc musl-dev libxml2-dev libxslt-dev 

RUN pip install -r requirements.txt
CMD ["watch", "-n", "180", "python3", "scrape_everything.py"]