from enum import Enum

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from morai_msgs.msg import SkidCtrlCmd
from morai_msgs.msg import SkidModel
from morai_msgs.msg import WheelRpm
from morai_msgs.msg import WheelTorque
import rclpy
from rclpy.node import Node


class CmdType(Enum):
    KEYBOARD = 0
    RPM_CONTROL = 1
    VELOCITY_CONTROL = 2


class PubSkidCtrlCmd(Node):
    def __init__(self):
        super().__init__("SkidCtrlCmd")
        self.topic = '/SkidCtrlCmd'
        self.publisher_ = self.create_publisher(SkidCtrlCmd, self.topic, 10)
  
    def publish_msg(self, param):
        msg = SkidCtrlCmd()
        msg.cmd_type = param["cmd_type"]
        msg.skid_model_ctrl = SkidModel()
        msg.skid_model_ctrl.rpm = WheelRpm()
        msg.skid_model_ctrl.rpm.left_front_wheel_rpm = self.clipping_rpm(param["skid_model_ctrl"]["rpm"]["left_front_wheel"])
        msg.skid_model_ctrl.rpm.left_rear_wheel_rpm = self.clipping_rpm(param["skid_model_ctrl"]["rpm"]["left_rear_wheel"])
        msg.skid_model_ctrl.rpm.right_front_wheel_rpm = self.clipping_rpm(param["skid_model_ctrl"]["rpm"]["right_front_wheel"])
        msg.skid_model_ctrl.rpm.right_rear_wheel_rpm = self.clipping_rpm(param["skid_model_ctrl"]["rpm"]["right_rear_wheel"])
        msg.skid_model_ctrl.torque = WheelTorque()
        msg.skid_model_ctrl.torque.left_front_wheel_torque_off = param["skid_model_ctrl"]["torque"]["left_front_wheel"] 
        msg.skid_model_ctrl.torque.left_rear_wheel_torque_off = param["skid_model_ctrl"]["torque"]["left_rear_wheel"] 
        msg.skid_model_ctrl.torque.right_front_wheel_torque_off = param["skid_model_ctrl"]["torque"]["right_front_wheel"] 
        msg.skid_model_ctrl.torque.right_rear_wheel_torque_off = param["skid_model_ctrl"]["torque"]["right_rear_wheel"] 
        msg.velocity_ctrl = Twist()
        msg.velocity_ctrl.linear = Vector3()
        msg.velocity_ctrl.linear.x = param["velocity_ctrl"]["linear"]
        msg.velocity_ctrl.linear.y = 0.0
        msg.velocity_ctrl.linear.z = 0.0
        msg.velocity_ctrl.angular = Vector3()
        msg.velocity_ctrl.angular.x = 0.0
        msg.velocity_ctrl.angular.y = 0.0
        msg.velocity_ctrl.angular.z = param["velocity_ctrl"]["angular"]
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing on {self.topic} : {msg}')
    
    def clipping_rpm(self, rpm):
        if rpm < -1000.0:
            return -1000.0
        elif rpm > 1000.0:
            return 1000.0
        else:
            return rpm
    
    def clipping_longitudinal_velocity(self, velocity):
        if velocity < -1.9:
            return -1.9
        elif velocity > 1.9:
            return 1.9
        else:
            return velocity
    
    def clipping_lateral_velocity(self, velocity):
        if velocity < -1.1:
            return -1.1
        elif velocity > 1.1:
            return 1.1
        else:
            return velocity


def main(args=None):
    rclpy.init(args=args)

    publisher = PubSkidCtrlCmd()
    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
