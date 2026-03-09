from morai_ros2_msgs.msg import IntersectionControl

import rclpy
from rclpy.node import Node
from std_msgs.msg import Header


class PubInsnControl(Node):
    def __init__(self):
        super().__init__("IntsnControl")
        self.topic = '/intersection_control'
        self.publisher_ = self.create_publisher(IntersectionControl, self.topic, 10)
        
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        stamp = self.get_clock().now().to_msg()
        msg = IntersectionControl()
        msg.header = Header()
        msg.header.stamp.sec = stamp.sec
        msg.header.stamp.nanosec = stamp.nanosec
        msg.intersection_index = 2
        msg.intersection_status = 1
        msg.intersection_status_time = 0.
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing on {self.topic} : {msg}')

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




