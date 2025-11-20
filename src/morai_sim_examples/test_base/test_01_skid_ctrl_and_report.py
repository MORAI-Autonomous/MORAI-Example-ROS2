from enum import Enum
import time

from morai_sim_examples.publishers.pub_skid_ctrl_cmd import CmdType
from morai_sim_examples.publishers.pub_skid_ctrl_cmd import PubSkidCtrlCmd
from morai_sim_examples.subscribers.sub_skid_ctrl_report import SubSkidCtrlReport
from morai_sim_examples.clients.morai_client_event_cmd import ClientEventCmdAsync
import pytest
import rclpy
from rclpy.executors import MultiThreadedExecutor


class Wheel(Enum):
    LEFT_FRONT = 0
    LEFT_REAR = 1
    RIGHT_FRONT = 2
    RIGHT_REAR = 3


class Test01SkidCtrlCmdAndReportBase:
    msgs_rx = []
    sub = None
    pub = None
    client = None
    executor = None
    skid_ctrl_cmd = {}

    @classmethod
    def setup_class(cls) -> None:
        rclpy.init()
        cls.pub = PubSkidCtrlCmd()
        cls.sub = SubSkidCtrlReport()
        cls.set_vehicle_auto_mode()
        cls.executor = MultiThreadedExecutor()
        cls.executor.add_node(cls.pub)
        cls.executor.add_node(cls.sub)
    
    @classmethod
    def teardown_class(cls) -> None:
        cls.pub.destroy_node()
        cls.sub.destroy_node()
        cls.executor.shutdown()
        rclpy.shutdown()
    
    @pytest.fixture
    def setup_teardown_method(self):
        self.msgs_rx.clear()
        self.skid_ctrl_cmd = {
            'cmd_type': CmdType.RPM_CONTROL,
            'skid_model_ctrl' : {
                'rpm' : {
                    'left_front_wheel' : 0.0,
                    'left_rear_wheel' : 0.0,
                    'right_front_wheel' : 0.0,
                    'right_rear_wheel' : 0.0
                },
                'torque' : {
                    'left_front_wheel' : False,
                    'left_rear_wheel' : False,
                    'right_front_wheel' : False,
                    'right_rear_wheel' : False
                }
            },
            'velocity_ctrl' : {
                'linear' : 0.0,
                'angular' : 0.0
            }
        }
        yield time.sleep(3)
        self.init_rpm()
        self.init_velocity()
        time.sleep(3)

    @classmethod
    def set_vehicle_auto_mode(cls):
        client = ClientEventCmdAsync()
        client.send_request()

        while rclpy.ok():
            rclpy.spin_once(client)
            if client.future.done():
                result_msg = client.future.result()
                break
    
    def init_rpm(self):
        self.publish(self.rpm_control([0.0, 0.0, 0.0, 0.0], [False, False, False, False]))
    
    def init_velocity(self):
        self.publish(self.velocity_control(0.0, 0.0))
    
    def rpm_control(self, rpm, torque_off):
        self.skid_ctrl_cmd['cmd_type'] = CmdType.RPM_CONTROL.value
        self.skid_ctrl_cmd['skid_model_ctrl']['rpm']['left_front_wheel'] = rpm[Wheel.LEFT_FRONT.value]
        self.skid_ctrl_cmd['skid_model_ctrl']['rpm']['left_rear_wheel'] = rpm[Wheel.LEFT_REAR.value]
        self.skid_ctrl_cmd['skid_model_ctrl']['rpm']['right_front_wheel'] = rpm[Wheel.RIGHT_FRONT.value]
        self.skid_ctrl_cmd['skid_model_ctrl']['rpm']['right_rear_wheel'] = rpm[Wheel.RIGHT_REAR.value]
        self.skid_ctrl_cmd['skid_model_ctrl']['torque']['left_front_wheel'] = torque_off[Wheel.LEFT_FRONT.value]
        self.skid_ctrl_cmd['skid_model_ctrl']['torque']['left_rear_wheel'] = torque_off[Wheel.LEFT_REAR.value]
        self.skid_ctrl_cmd['skid_model_ctrl']['torque']['right_front_wheel'] = torque_off[Wheel.RIGHT_FRONT.value]
        self.skid_ctrl_cmd['skid_model_ctrl']['torque']['right_rear_wheel'] = torque_off[Wheel.RIGHT_REAR.value]
        return self.skid_ctrl_cmd
    
    def velocity_control(self, longitudinal_velocity, lateral_velocity):
        self.skid_ctrl_cmd['cmd_type'] = CmdType.VELOCITY_CONTROL.value
        self.skid_ctrl_cmd['velocity_ctrl']['linear'] = longitudinal_velocity
        self.skid_ctrl_cmd['velocity_ctrl']['angular'] = lateral_velocity
        return self.skid_ctrl_cmd
    
    def publish(self, skid_ctrl_cmd):
        self.pub.publish_msg(skid_ctrl_cmd)
    
    def get_skid_ctrl_report(self):
        time.sleep(1)
        received = None
        self.sub.received.clear()
        try:
            while rclpy.ok():
                self.executor.spin_once(timeout_sec=1.0)
                if len(self.sub.received) > 2:
                    break
            received = self.sub.received.pop()
        finally:
            return received

