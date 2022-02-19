FROM ros:galactic
# FROM osrf/ros:galactic-desktop

RUN mkdir -p /home

COPY ros2_ultrasonic_sensor /home/ros2_ultrasonic_sensor

RUN cd /home && \
  rosdep install -i --from-path /home --rosdistro galactic -y && \
  colcon build --packages-select ros2_ultrasonic_sensor

SHELL ["/bin/bash", "-c"]
CMD . /home/install/setup.bash && ros2 run ros2_ultrasonic_sensor talker