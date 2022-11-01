FROM python:3.9
WORKDIR /tmp
COPY requirements.txt .
RUN pip install -r requirements.txt
