FROM python:3.11-slim-bookworm
WORKDIR /app

# must be called from the project root directory to copy requirements.txt
COPY requirements.txt /app/requirements.txt
# install project dependencies
RUN pip install -r requirements.txt
# create folder structure for bind mounts
RUN mkdir -p /app/test/output && mkdir /app/BoardManager
# This image can be used for testing, documenting, ... No entrypoint or command needed
