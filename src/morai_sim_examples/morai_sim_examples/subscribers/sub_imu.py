import rclpy
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy

from sensor_msgs.msg import Imu


class SubImuMessage(Node):
    def __init__(self):
        super().__init__("ImuMessage")
        
        self.topic = "/Imu"
        self.declare_parameter("qos_depth", 10)
        qos_depth = self.get_parameter("qos_depth").value
        QoS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE,
        )
        self.subscription = self.create_subscription(Imu, self.topic, self.callback, QoS_RKL10V)
  
    def callback(self, msg):
        self.get_logger().info(f'[Subscription] {self.topic} : {msg}')

def main(args=None):
    rclpy.init(args=args)
    subscriber = SubImuMessage()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
