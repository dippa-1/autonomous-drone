FROM python:alpine

COPY requirements.txt ./

RUN apk --update add gcc make g++ zlib-dev py3-curl
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /benchmarks

COPY . .

CMD ["python", "./requests_client.py"]
