FROM python:3.10-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get -y install gcc libpq-dev libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev

# Install pip packages
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy code to working dir
COPY . .

# Run the crawler as a cronjob when the container launches
CMD [ "python3", "./cronjob_spider.py" ]
