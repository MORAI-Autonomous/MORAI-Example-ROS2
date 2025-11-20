from morai_msgs.msg import IntersectionControl

import rclpy
from rclpy.node import Node
from std_msgs.msg import Header


class PubInsnControl(Node):
    def __init__(self):
        super().__init__("IntsnControl")
        self.topic = '/InsnControl'
        self.publisher_ = self.create_publisher(IntersectionControl, self.topic, 10)
  
    def publish_msg(self, param):
        stamp = self.get_clock().now().to_msg()
        msg = IntersectionControl()
        msg.header = Header()
        msg.header.stamp.sec = stamp.sec
        msg.header.stamp.nanosec = stamp.nanosec
        msg.intersection_index = param['intersection_index']
        msg.intersection_status = param['intersection_status']
        msg.intersection_status_time = param['intersection_status_time']
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    publisher = PubInsnControl()
    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()




