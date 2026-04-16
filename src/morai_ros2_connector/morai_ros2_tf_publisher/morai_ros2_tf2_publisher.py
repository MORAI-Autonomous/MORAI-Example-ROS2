#!/usr/bin/env python3
import argparse
import json
import math
import os

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage


# Maps each sensor list key to its per-sensor config sub-key in the JSON.
# The config sub-object holds rosConfig / ros2NativeConfig with the frameID.
SENSOR_CONFIG_KEY = {
    'cameraList':     'cc',
    'Lidar3DList':    'lc',
    'Lidar2DList':    'lc',
    'GPSList':        'gc',
    'IMUList':        'ic',
    'RadarList':      'rc',
    'Radar4DList':    'rc',
    'UltrasonicList': 'uc',
}


def euler_to_quaternion(roll_deg, pitch_deg, yaw_deg):
    """Convert ZYX Euler angles (degrees) to quaternion (x, y, z, w).

    Rotation order: yaw around Z, pitch around Y, roll around X.
    Matches the ROS convention used by tf2.
    """
    roll  = math.radians(roll_deg)
    pitch = math.radians(pitch_deg)
    yaw   = math.radians(yaw_deg)

    cy, sy = math.cos(yaw * 0.5),   math.sin(yaw * 0.5)
    cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
    cr, sr = math.cos(roll * 0.5),  math.sin(roll * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy

    return qx, qy, qz, qw


def parse_sensor_transforms(json_path):
    """Read sensor pos/rot entries from a MORAI sensor config JSON file.

    Returns a list of dicts, each with:
        frame_id, x, y, z  (meters)
        roll, pitch, yaw   (degrees)
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    transforms = []
    for list_key, config_key in SENSOR_CONFIG_KEY.items():
        for sensor in data.get(list_key, []):
            pos = sensor.get('pos', {})
            rot = sensor.get('rot', {})

            # Resolve frameID: prefer ros2NativeConfig (26.R1+), fall back to
            # rosConfig (legacy bridge format), then generate a fallback name.
            config = sensor.get(config_key, {})
            ros2_native = config.get('ros2NativeConfig', {})
            ros_config   = config.get('rosConfig', {})
            frame_id = (
                ros2_native.get('frameID', '').strip()
                or ros_config.get('frameID', '').strip()
            )
            if not frame_id:
                uid = sensor.get('m_SensorUniqueID', 'unknown')
                frame_id = f'sensor_{uid}'

            transforms.append({
                'frame_id': frame_id,
                'x':     float(pos.get('x', 0.0)),
                'y':     float(pos.get('y', 0.0)),
                'z':     float(pos.get('z', 0.0)),
                'roll':  float(rot.get('roll',  0.0)),
                'pitch': float(rot.get('pitch', 0.0)),
                'yaw':   float(rot.get('yaw',   0.0)),
            })

    return transforms


class TF2SensorPublisher(Node):
    def __init__(self, transforms, parent_frame, topic):
        super().__init__('morai_tf2_sensor_publisher')

        # TRANSIENT_LOCAL so that late-joining subscribers still receive the
        # transforms (mirrors the behaviour of tf2_ros.StaticTransformBroadcaster).
        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.publisher_ = self.create_publisher(TFMessage, topic, qos)
        self._transforms = transforms
        self._parent_frame = parent_frame
        self._topic = topic

    def publish(self):
        """Build and send a TFMessage containing all sensor transforms."""
        tf_msg = TFMessage()
        now = self.get_clock().now().to_msg()

        for t in self._transforms:
            ts = TransformStamped()
            ts.header.stamp = now
            ts.header.frame_id = self._parent_frame
            ts.child_frame_id  = t['frame_id']

            ts.transform.translation.x = t['x']
            ts.transform.translation.y = t['y']
            ts.transform.translation.z = t['z']

            qx, qy, qz, qw = euler_to_quaternion(t['roll'], t['pitch'], t['yaw'])
            ts.transform.rotation.x = qx
            ts.transform.rotation.y = qy
            ts.transform.rotation.z = qz
            ts.transform.rotation.w = qw

            tf_msg.transforms.append(ts)

        self.publisher_.publish(tf_msg)

        for t in self._transforms:
            self.get_logger().info(
                f'{self._parent_frame} -> {t["frame_id"]}  '
                f'pos=({t["x"]:.3f}, {t["y"]:.3f}, {t["z"]:.3f})  '
                f'rpy=({t["roll"]:.3f}\u00b0, {t["pitch"]:.3f}\u00b0, {t["yaw"]:.3f}\u00b0)'
            )
        self.get_logger().info(
            f'Published {len(self._transforms)} transform(s) on {self._topic}'
        )


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Read MORAI sensor config JSON and broadcast sensor-to-vehicle '
            'TF2 transforms over ROS2.'
        )
    )
    parser.add_argument(
        '-f', '--json-file',
        required=True,
        metavar='PATH',
        help='Path to the MORAI sensor config JSON file (e.g. test_ros2.json)',
    )
    parser.add_argument(
        '-t', '--topic',
        default='/tf_static',
        metavar='TOPIC',
        help='ROS2 topic to publish TFMessage on (default: /tf_static)',
    )
    parser.add_argument(
        '-p', '--parent-frame',
        default='base_link',
        metavar='FRAME',
        help='Parent frame ID for all sensor transforms (default: base_link)',
    )
    args = parser.parse_args()

    if not os.path.isfile(args.json_file):
        print(f'Error: JSON file not found: {args.json_file}')
        exit(-1)

    try:
        transforms = parse_sensor_transforms(args.json_file)
    except Exception as e:
        print(f'Error parsing JSON: {e}')
        exit(-1)

    if not transforms:
        print('No sensor transforms found in the JSON file.')
        exit(0)

    print(f'Loaded {len(transforms)} sensor transform(s) from {args.json_file}')

    rclpy.init()
    node = TF2SensorPublisher(transforms, args.parent_frame, args.topic)
    executor = SingleThreadedExecutor()
    executor.add_node(node)

    try:
        # Publish once, then keep the node alive so TRANSIENT_LOCAL durability
        # continues to serve the message to late-joining subscribers.
        node.publish()
        executor.spin()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Error: {e}')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
