FROM ubuntu:impish

COPY requirements.txt ./

RUN apt update && apt install python3 python3-pip -y
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8001 8002 8003 8004 8005 8006 8007

CMD ["python3", "./run_servers.py"]
