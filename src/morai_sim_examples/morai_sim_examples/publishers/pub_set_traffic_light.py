from enum import Enum

import rclpy
from rclpy.node import Node

from morai_msgs.msg import SetTrafficLight


""" 신호등 색상 """
class LightColors(Enum):
    """ 불이 꺼져있는 상태 """
    NONE = 0
    """ 신호등이 초기화 되지 않았을 때 """
    UNDEFINED = -1
    """ 신호등을 찾지 못했을 때 """
    DETECTED = -2

    """ Red """
    R = 1
    """ Yellow """
    Y = 4
    """ Straight Green >> 직진 녹색 """
    SG = 16
    """ Left Green >> ← 좌회전 녹색 """
    LG = 32
    """ Right Green >> → 우회전 녹색 """
    RG = 64
    """ UTurn Green  """
    UTG = 128
    """ Upper Left Green >> ↖ """
    ULG = 256
    """ Upper Right Green >> ↗ """
    URG = 512
    """ Lower Left Green >> ↙ """
    LLG = 1024
    """ Lower Right Green >> ↘  """
    LRG = 2048
    
    """ R | Y """
    R_WITH_Y = 5
    """ Y | SG """
    Y_WITH_G = 20
    """ Y | LG """
    Y_WITH_GLEFT = 36
    """ SG | LG """
    G_WITH_GLEFT = 48
    """ R | LG """
    R_WITH_GLEFT = 33
    """ SG | LLG """
    LLG_SG = 1040
    """ R | LLG """
    R_LLG = 1025
    """ ULG | URG """
    ULG_URG = 768

class PubSetTrafficLight(Node):
    def __init__(self):
        super().__init__("SetTrafficLight")
        self.topic = '/SetTrafficLight'
        self.publisher_ = self.create_publisher(SetTrafficLight, self.topic, 10)
  
    def publish_msg(self, param):
        msg = SetTrafficLight()
        msg.traffic_light_index = param['traffic_light_index']
        msg.traffic_light_status = param['traffic_light_status']
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    publisher = PubSetTrafficLight()
    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()




