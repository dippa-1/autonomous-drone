# FROM arm64v8/ros:galactic
FROM ros:galactic

# VOLUME "./ros2-pkgs"

COPY requirements.txt ./

RUN apt-get update && apt-get install wget python3-pip -y
RUN pip install --no-cache-dir -r requirements.txt


COPY ./create_ros2_package.sh /
