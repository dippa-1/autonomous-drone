FROM python:alpine

COPY requirements.txt ./

RUN apk --update add gcc make g++ zlib-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8001 8002 8003 8004 8005 8006 8007

CMD ["python", "./run_servers.py"]
