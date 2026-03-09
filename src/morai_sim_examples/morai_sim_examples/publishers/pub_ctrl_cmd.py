from enum import Enum

from morai_ros2_msgs.msg import CtrlCmd
import rclpy
from rclpy.node import Node

from rosidl_runtime_py import message_to_ordereddict

class LongCmdType(Enum):
    NONE = 0
    THROTTLE = 1
    VELOCITY = 2
    ACCELERATION = 3


class PubCtrlCmd(Node):
    def __init__(self):
        super().__init__("CtrlCmd")
        self.topic = '/ctrl_cmd_0'
        self.publisher_ = self.create_publisher(CtrlCmd, self.topic, 10)

        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        msg = CtrlCmd()
        msg.longl_cmd_type = 1
        msg.accel = 0.5
        msg.brake = 0.1
        msg.front_steer = 0.5
        msg.velocity = 0.
        msg.acceleration = 0.
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




