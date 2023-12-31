FROM python:3.11
WORKDIR /usr/src/hightech
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./wait-for-it.sh .
COPY ./script.sh .
RUN chmod +x ./wait-for-it.sh
RUN chmod +x ./script.sh
RUN pip install -r requirements.txt
COPY . .