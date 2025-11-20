import rclpy
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy

from morai_msgs.msg import GetTrafficLightStatus


class SubGetTrafficLightStatus(Node):
    def __init__(self):
        super().__init__("GetTrafficLightStatus")
        self.received = []
        self.topic = "/GetTrafficLightStatus"
        self.declare_parameter("qos_depth", 10)
        qos_depth = self.get_parameter("qos_depth").value
        QoS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE,
        )
        self.subscription = self.create_subscription(GetTrafficLightStatus, self.topic, self.callback, QoS_RKL10V)
  
    def callback(self, msg):
        self.received.append(msg)

def main(args=None):
    rclpy.init(args=args)
    subscriber = SubGetTrafficLightStatus()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
