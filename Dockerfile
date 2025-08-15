# syntax=docker/dockerfile:1

FROM python:alpine3.22
WORKDIR /cerpadlo
COPY . .
RUN pip install -r requirements.txt
CMD ["watch", "-n", "180", "python3", "scrape_everything.py"]


