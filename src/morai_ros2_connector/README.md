# ROS2 Connector Scripts

## morai_ros2_connector

Provides ROS2 connection intialization when using the custom MORAI-ROS2 bridge executable script. Refer to the main [readme](/README.md) for usage instructions.

morai_ros2_connector is intended for use with MORAI SIM 24.R2 or older.

## morai_ros2_tf_publisher

### Notice

Intended to be used solely with MORAI SIM 26.R1.26R1 (released April 2026)

### Use

This script is a workaround for MORAI SIM 26.R1.26R1, which added features to support ROS2 natively within the simulator, but did not adjust its tf2 publisher to adopt updates to ROS2.

morai_ros2_tf_publisher reads a sensor configuration JSON file to determine the relative positions and orientations of each sensor model attached to the egovehicle. Requires a sensor configuration JSON file from MORAI SIM. These files are typically auto-saved in the following path: `[your MORAI SIM install folder]/MoraiLauncher_Win_Data\SaveFile\Sensor\26.R1.26R1`

**Arguments**
- `-f`: (required) points to the JSON file your sensor configuration is saved in
- `-t`: change the topic name of the tf2 publisher (default is `tf2_static`)
- `-p`: change the name of the parent frame ID (default is `base_link`)

## morai_camera_info_publisher

### Notice

Intended to be used solely with MORAI SIM 26.R1.26R1 (released April 2026)

### Use

This script reads a sensor configuration JSON file and publishes `sensor_msgs/CameraInfo` for each camera attached to the ego vehicle. It derives camera intrinsics (focal lengths, principal point, distortion coefficients) directly from the simulator's sensor parameters, allowing downstream ROS2 nodes such as image processing pipelines to receive calibration data without manual configuration.

Camera intrinsics are computed as follows:
- `fx = focalLengthmm × cameraResWidth / sensorSize.x`
- `fy = focalLengthmm × cameraResHeight / sensorSize.y`
- `cx`, `cy` from `principalPoint`
- Distortion coefficients `[k1, k2, p1, p2, k3]` from `lensDistortion`

The CameraInfo topic is derived automatically from the sensor JSON:
- For 26.R1+ files, the image topic in `ros2NativeConfig.Topic` (e.g. `/camera/image/compressed`) has its image suffix replaced with `camera_info` (e.g. `/camera/camera_info`).
- For older files without a topic, the `-t` fallback value is used.

The node publishes once on startup and then stays alive, so late-joining subscribers still receive the calibration data (TRANSIENT_LOCAL QoS).

Requires a sensor configuration JSON file from MORAI SIM. These files are typically auto-saved in the following path: `[your MORAI SIM install folder]/MoraiLauncher_Win_Data\SaveFile\Sensor\26.R1.26R1`

**Arguments**
- `-f`: (required) path to the JSON file your sensor configuration is saved in
- `-t`: fallback topic name used when the JSON contains no topic (default: `/camera/camera_info`). For multi-camera JSONs without topics, each camera publishes on `<topic>/<frame_id>`
