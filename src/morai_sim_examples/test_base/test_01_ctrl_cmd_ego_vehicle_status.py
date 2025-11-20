from enum import Enum
import time

from morai_sim_examples.publishers.pub_ctrl_cmd import LongCmdType
from morai_sim_examples.publishers.pub_ctrl_cmd import PubCtrlCmd
from morai_sim_examples.subscribers.sub_ego_vehicle_status import SubEgoVehicleStatus
from morai_sim_examples.clients.morai_client_event_cmd import ClientEventCmdAsync
import pytest
import rclpy
from rclpy.executors import MultiThreadedExecutor


class LonglCmdType(Enum):
    NONE = 0
    THROTTLE = 1
    VELOCITY = 2
    ACCELERATION = 3


class Test01CtrlCmdAndEgoVehicleStatusBase:
    msgs_rx = []
    sub = None
    pub = None
    client = None
    executor = None
    ctrl_cmd = {}

    @classmethod
    def setup_class(cls) -> None:
        rclpy.init()
        cls.pub = PubCtrlCmd()
        cls.sub = SubEgoVehicleStatus()
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
        self.ctrl_cmd = {
            'longlCmdType': LongCmdType.NONE.value,
            'accel': 0.0,
            'brake': 0.0,
            'steering': 0.0,
            'velocity': 0.0,
            'acceleration': 0.0
        }
        yield time.sleep(3)
        self.init_velocity()

    @classmethod
    def set_vehicle_auto_mode(cls):
        client = ClientEventCmdAsync()
        client.send_request()

        while rclpy.ok():
            rclpy.spin_once(client)
            if client.future.done():
                result_msg = client.future.result()
                break
    
    def init_velocity(self):
        self.publish(self.throttle_control(0.0, 0.0, 0.0))
    
    def throttle_control(self, accel, brake, steering):
        self.ctrl_cmd['longlCmdType'] = LongCmdType.THROTTLE.value
        self.ctrl_cmd['accel'] = accel
        self.ctrl_cmd['brake'] = brake
        self.ctrl_cmd['steering'] = steering
        return self.ctrl_cmd
    
    def velocity_control(self, velocity, steering):
        self.ctrl_cmd['longlCmdType'] = LongCmdType.VELOCITY.value
        self.ctrl_cmd['velocity'] = velocity
        self.ctrl_cmd['steering'] = steering
        return self.ctrl_cmd
    
    def acceleration_control(self, acceleration, steering):
        self.ctrl_cmd['longlCmdType'] = LongCmdType.ACCELERATION.value
        self.ctrl_cmd['acceleration'] = acceleration
        self.ctrl_cmd['steering'] = steering
        return self.ctrl_cmd
    
    def publish(self, ctrl_cmd):
        self.pub.publish_msg(ctrl_cmd)
    
    def get_ego_vehicle_status(self):
        time.sleep(1)
        received = None
        try:
            while rclpy.ok():
                self.executor.spin_once(timeout_sec=1.0)
                if len(self.sub.received) > 2:
                    break
            received = self.sub.received.pop()
        finally:
            return received

