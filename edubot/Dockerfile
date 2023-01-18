
# Base Image
FROM python:3.9.6-alpine

# Copy requirements
COPY requirements.txt /tmp/requirements.txt
RUN apk update && apk add postgresql-dev postgresql-client gcc python3-dev musl-dev
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Set Environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy Project
COPY . /app   

EXPOSE 80

# Set Work Directory
WORKDIR /app

