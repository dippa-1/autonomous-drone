WORK_DIR=/ros2-pkgs
PKG_NAME=py_pubsub
cd $WORK_DIR
ros2 pkg create --build-type ament_python $PKG_NAME
wget https://raw.githubusercontent.com/ros2/examples/master/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py -P ./$PKG_NAME/$PKG_NAME
wget https://raw.githubusercontent.com/ros2/examples/master/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py -P ./$PKG_NAME/$PKG_NAME
sed -i '23 i \\t\t"talker = $PKG_NAME.publisher_member_function:main",\n\t\t"listener = $PKG_NAME.subscriber_member_function:main"' ./$PKG_NAME/setup.py
rosdep install -i --from-path $WORK_DIR --rosdistro galactic -y
colcon build --packages-select $PKG_NAME
. install/setup.bash
ros2 run $PKG_NAME talker &
ros2 run $PKG_NAME listener
