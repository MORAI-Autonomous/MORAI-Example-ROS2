import pytest
import time

from morai_sim_examples.publishers.pub_set_traffic_light import PubSetTrafficLight
from morai_sim_examples.publishers.pub_set_traffic_light import LightColors
from morai_sim_examples.subscribers.sub_traffic_light_status import SubGetTrafficLightStatus
import rclpy
from rclpy.executors import MultiThreadedExecutor

class Test02SetTrafficLightAndStatusBase:
    msgs_rx = []
    sub = None
    pub = None
    executor = None
    traffic_light_param = {
        'traffic_light_index' : 'None',
        'traffic_light_status' : LightColors.NONE.value
    }

    @classmethod
    def setup_class(cls) -> None:
        rclpy.init()
        cls.pub = PubSetTrafficLight()
        cls.sub = SubGetTrafficLightStatus()
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
        self.traffic_light_param['traffic_light_index'] = 'None'
        self.traffic_light_param['traffic_light_status'] = LightColors.NONE.value
        yield time.sleep(1)
    
    def set_traffic_light(self, traffic_light_id: str, color: LightColors):
        self.traffic_light_param['traffic_light_index'] = traffic_light_id
        self.traffic_light_param['traffic_light_status'] = color.value
        return self.traffic_light_param
    
    def publish(self, traffic_light_param):
        self.pub.publish_msg(traffic_light_param)
    
    def get_traffic_light_status(self):
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


