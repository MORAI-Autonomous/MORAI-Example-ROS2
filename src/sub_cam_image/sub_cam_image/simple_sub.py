import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError

class SubCompressedImage(Node):
  def __init__(self) -> None:
    super().__init__("CameraSensor")
    self.bridge = CvBridge()
    self.subscription = self.create_subscription(CompressedImage, "/image_jpeg/compressed", self.callback, 10)
  
  def callback(self, data):
    cv_image = self.bridge.compressed_imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("received image", cv_image)
    cv2.waitKey(1)

def main(args=None):
  rclpy.init(args=args)
  camera = SubCompressedImage()
  rclpy.spin(camera)
  camera.destroy_node()
  rclpy.shutdown()

if __name__ == "__main__":
  main()
