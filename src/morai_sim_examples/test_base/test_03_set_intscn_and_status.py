import pytest
import time

from morai_sim_examples.publishers.pub_intsn_control import PubInsnControl
from morai_sim_examples.subscribers.sub_intersection_status import SubIntersectionStatus
import rclpy
from rclpy.executors import MultiThreadedExecutor


class Test03SetIntscnAndStatusBase:
    msgs_rx = []
    sub = None
    pub = None
    executor = None
    intersection_param = {
        'intersection_index': 'None',
        'intersection_status': 0,
        'intersection_status_time': 0.0
    }

    @classmethod
    def setup_class(cls) -> None:
        rclpy.init()
        cls.pub = PubInsnControl()
        cls.sub = SubIntersectionStatus()
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
        self.intersection_param['intersection_index'] = 'None'
        self.intersection_param['intersection_status'] = 0
        self.intersection_param['intersection_status_time'] = 0.0
        yield time.sleep(1)
    
    def set_intersection_status(self, intersection_id: int, status: int):
        self.intersection_param['intersection_index'] = intersection_id
        self.intersection_param['intersection_status'] = status
        self.intersection_param['intersection_status_time'] = 0.0
        return self.intersection_param
    
    def publish(self, intersection_param):
        self.pub.publish_msg(intersection_param)
    
    def get_intersection_status(self):
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

