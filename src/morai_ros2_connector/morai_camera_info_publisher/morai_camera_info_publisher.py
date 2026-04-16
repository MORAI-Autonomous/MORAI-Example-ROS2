#!/usr/bin/env python3
import argparse
import json
import os
import re

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from sensor_msgs.msg import CameraInfo


# Matches common image-topic suffixes that should be replaced with camera_info.
_IMAGE_SUFFIX_RE = re.compile(
    r'(?:image(?:/compressed|/raw|_raw|_compressed))$'
)


def _derive_topic(cc, fallback_topic, frame_id, n_cameras):
    """Return the CameraInfo topic for a single camera config block."""
    for config_key in ('ros2NativeConfig', 'rosConfig'):
        raw = cc.get(config_key, {}).get('Topic', '').strip()
        if not raw:
            continue
        substituted = _IMAGE_SUFFIX_RE.sub('camera_info', raw)
        if substituted != raw:
            return substituted
        # Non-empty topic but unrecognised suffix — append camera_info namespace.
        if not raw.endswith('camera_info'):
            return raw.rstrip('/') + '/camera_info'
        return raw

    # No topic found in JSON; use CLI fallback.
    if n_cameras == 1:
        return fallback_topic
    return fallback_topic.rstrip('/') + '/' + frame_id


def parse_camera_infos(json_path, fallback_topic):
    """Parse camera calibration data from a MORAI sensor config JSON file.

    Returns a list of dicts, each containing:
        topic, frame_id, width, height,
        K (9 floats), D (5 floats), R (9 floats), P (12 floats),
        distortion_model
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    camera_list = data.get('cameraList', [])
    n_cameras = len(camera_list)
    results = []

    for camera in camera_list:
        cc = camera.get('cc', {})

        focal_mm = float(cc.get('focalLengthmm', 0.0))
        sensor   = cc.get('sensorSize', {})
        sx       = float(sensor.get('x', 0.0))
        sy       = float(sensor.get('y', 0.0))
        pp       = cc.get('principalPoint', {})
        cx       = float(pp.get('x', 0.0))
        cy       = float(pp.get('y', 0.0))
        width    = int(cc.get('cameraResWidth',  0))
        height   = int(cc.get('cameraResHeight', 0))
        raw_dist = list(cc.get('lensDistortion', []))

        # Derive focal lengths in pixels; guard against zero sensor size.
        fx = (focal_mm * width  / sx) if sx != 0.0 else 0.0
        fy = (focal_mm * height / sy) if sy != 0.0 else 0.0

        K = [fx,  0.0, cx,
             0.0, fy,  cy,
             0.0, 0.0, 1.0]

        R = [1.0, 0.0, 0.0,
             0.0, 1.0, 0.0,
             0.0, 0.0, 1.0]

        P = [fx,  0.0, cx,  0.0,
             0.0, fy,  cy,  0.0,
             0.0, 0.0, 1.0, 0.0]

        # Pad or trim lensDistortion to exactly 5 floats [k1, k2, p1, p2, k3].
        D = (raw_dist + [0.0, 0.0, 0.0, 0.0, 0.0])[:5]

        # frame_id: prefer ros2NativeConfig (26.R1+), fall back to rosConfig.
        ros2_native = cc.get('ros2NativeConfig', {})
        ros_config  = cc.get('rosConfig', {})
        frame_id = (
            ros2_native.get('frameID', '').strip()
            or ros_config.get('frameID', '').strip()
            or f'camera_{camera.get("m_SensorUniqueID", "unknown")}'
        )

        topic = _derive_topic(cc, fallback_topic, frame_id, n_cameras)

        results.append({
            'topic':            topic,
            'frame_id':         frame_id,
            'width':            width,
            'height':           height,
            'K':                K,
            'D':                D,
            'R':                R,
            'P':                P,
            'distortion_model': 'plumb_bob',
        })

    return results


class CameraInfoPublisher(Node):
    def __init__(self, camera_infos):
        super().__init__('morai_camera_info_publisher')

        # TRANSIENT_LOCAL so late-joining subscribers still receive calibration.
        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
        )

        self._entries = []
        for info in camera_infos:
            pub = self.create_publisher(CameraInfo, info['topic'], qos)

            msg = CameraInfo()
            msg.header.frame_id  = info['frame_id']
            msg.width            = info['width']
            msg.height           = info['height']
            msg.distortion_model = info['distortion_model']
            msg.d                = info['D']
            msg.k                = info['K']
            msg.r                = info['R']
            msg.p                = info['P']
            # header.stamp is set at publish time from the live clock.

            self._entries.append((pub, msg, info['topic']))

    def publish(self):
        """Stamp and publish CameraInfo for every camera."""
        now = self.get_clock().now().to_msg()
        for pub, msg, topic in self._entries:
            msg.header.stamp = now
            pub.publish(msg)
            self.get_logger().info(
                f'Published CameraInfo on {topic} '
                f'[{msg.width}x{msg.height}] frame_id={msg.header.frame_id}'
            )


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Read MORAI sensor config JSON and publish sensor_msgs/CameraInfo '
            'for each camera over ROS2.'
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
        default='/camera/camera_info',
        metavar='TOPIC',
        help=(
            'Fallback CameraInfo topic used when the JSON contains no topic '
            '(default: /camera/camera_info). For multi-camera JSONs without '
            'topics, each camera appends its frame_id to this value.'
        ),
    )
    args = parser.parse_args()

    if not os.path.isfile(args.json_file):
        print(f'Error: JSON file not found: {args.json_file}')
        exit(-1)

    try:
        camera_infos = parse_camera_infos(args.json_file, args.topic)
    except Exception as e:
        print(f'Error parsing JSON: {e}')
        exit(-1)

    if not camera_infos:
        print('No camera entries found in the JSON file.')
        exit(0)

    print(f'Loaded {len(camera_infos)} camera(s) from {args.json_file}')
    for info in camera_infos:
        print(f'  {info["frame_id"]} -> {info["topic"]}')

    rclpy.init()
    node = CameraInfoPublisher(camera_infos)
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
