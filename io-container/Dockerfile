FROM ubuntu:impish

COPY requirements.txt requirements.txt

# Setup lgpio
RUN apt update && apt upgrade -y && apt install python3-lgpio -y
RUN apt install python3-pip --no-install-recommends -y
RUN pip install -r requirements.txt
