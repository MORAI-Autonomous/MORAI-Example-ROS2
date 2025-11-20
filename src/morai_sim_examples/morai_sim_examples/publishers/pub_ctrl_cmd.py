from enum import Enum

from morai_msgs.msg import CtrlCmd
import rclpy
from rclpy.node import Node


class LongCmdType(Enum):
    NONE = 0
    THROTTLE = 1
    VELOCITY = 2
    ACCELERATION = 3


class PubCtrlCmd(Node):
    def __init__(self):
        super().__init__("CtrlCmd")
        self.topic = '/ctrl_cmd'
        self.publisher_ = self.create_publisher(CtrlCmd, self.topic, 10)
  
    def publish_msg(self, param):
        msg = CtrlCmd()
        msg.longl_cmd_type = param["longlCmdType"]
        msg.accel = param["accel"]
        msg.brake = param["brake"]
        msg.steering = param["steering"]
        msg.velocity = param["velocity"]
        msg.acceleration = param["acceleration"]
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing on {self.topic} : {msg}')

def main(args=None):
    rclpy.init(args=args)

    publisher = PubCtrlCmd()
    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()




