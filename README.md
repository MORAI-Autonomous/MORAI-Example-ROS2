[![MORAILog](./docs/MORAI_Logo.png)](https://www.morai.ai)
# MORAI-ROS2Example
MORAI Simulator OpenSource Example - ROS2 examples
```
./
├── src          
│    ├── morai_ros2_connector  # script for MORAI Simulator to open ROS2 service
│    ├── morai_ros2_msgs       # MORAI Simulator ROS2 message set
│    └── morai_sim_examples    # example ros2 nodes and unit testing codes
├── gRPC_ROS2_Bridge           # A Bridge to communicate MORAI SIM with ROS2

```

This example contains the below list.
  - ROS2 communication

# Requirement
- ROS2 desktop-full == eloquent
- python >= 3.6

# Installation
```
$ mkdir ~/ws_morai_sim_example
$ cd ~/ws_morai_sim_example
$ git clone -b ros2-eloquent https://github.com/MORAI-Autonomous/MORAI-ROS2Example.git .
$ source /opt/ros/eloquent/setup.bash
$ colcon build
$ source ./install/setup.bash
```
# Usage
```
$ source ./install/setup.bash
$ ./gRPC_ROS2_Bridge
```

