# morai_ros2_connector

Provides ROS2 connection intialization when using the custom MORAI-ROS2 bridge executable script. Refer to the main [readme](/README.md) for usage instructions.

# morai_ros2_tf_publisher

## Notice

Intended to be used solely with MORAI SIM 26.R1.26R1 (released April 2026)

## Use

This script is a workaround for MORAI SIM 26.R1.26R1, which added features to support ROS2 natively within the simulator, but did not adjust its tf2 publisher to adopt updates to ROS2.

morai_ros2_tf_publisher reads a sensor configuration JSON file to determine the relative positions and orientations of each sensor model attached to the egovehicle. Requires a sensor configuration JSON file from MORAI SIM. These files are typically auto-saved in the following path: `[your MORAI SIM install folder]/MoraiLauncher_Win_Data\SaveFile\Sensor\26.R1.26R1`

Arguments
- `-f`: (required) points to the JSON file your sensor configuration is saved in
- `-t`: change the topic name of the tf2 publisher (default is `tf2_static`)
- `-p`: change the name of the parent frame ID (default is `base_link`)
