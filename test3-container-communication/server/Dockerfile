FROM python:alpine

COPY requirements.txt ./

RUN apk --update add gcc make g++ zlib-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "./http_server.py"]
