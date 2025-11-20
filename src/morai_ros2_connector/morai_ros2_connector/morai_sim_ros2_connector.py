import argparse
from collections import defaultdict
from distutils.command.config import config
import os
import json
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy

from morai_msgs.msg import MoraiSimConfig

current_path = os.path.dirname(os.path.realpath(__file__))
file_path = current_path+'/'
file_name = 'morai_sim_ros2_config.json'


class MoraiConfigFileHandler:
    def __init__(self):
        self.support_type_list = []
    
    def load_support_types(self):
        with open(file=file_path+'support_types.json', mode='r') as fp:
            self.support_type_list = json.load(fp)

    def load_config(self):
        with open(file=file_path+file_name, mode='r') as fp:
            data = json.load(fp)
            converted = defaultdict(list)
            converted['publisherList'].extend(data['VehicleInterface'][0]['publisherList'] if 'publisherList' in data['VehicleInterface'][0] else [])
            self.__check_publisher_validity(converted['publisherList'])
            converted['cameraList'].extend(data['SensorInterface'][1]['cameraList'] if 'cameraList' in data['SensorInterface'][1] else [])
            self.__check_publisher_validity(converted['publisherList'])
            converted['GPSList'].extend(data['SensorInterface'][2]['GPSList'] if 'GPSList' in data['SensorInterface'][2] else [])
            self.__check_publisher_validity(converted['publisherList'])
            converted['IMUList'].extend(data['SensorInterface'][3]['IMUList'] if 'IMUList' in data['SensorInterface'][3] else [])
            self.__check_publisher_validity(converted['publisherList'])
            converted['subscriberList'].extend(data['VehicleInterface'][1]['subscriberList'] if 'subscriberList' in data['VehicleInterface'][1] else [])
            self.__check_subscriber_validity(converted['subscriberList'])
            converted['serviceList'].extend(data['VehicleInterface'][2]['serviceList'] if 'serviceList' in data['VehicleInterface'][2] else [])
            converted['sensorConfigFileName'] = data['SensorInterface'][0]['sensorConfigFileName'] if 'sensorConfigFileName' in data['SensorInterface'][0] else ""
            return converted
    
    def __check_publisher_validity(self, config):
        for item in config:
            if (item['ros2Config']['messageType'] not in self.support_type_list['supportMessageTypes'][0]['publisher']):
                raise Exception(f"Unsupported Message Type, {item['ros2Config']['messageType']}")
    
    def __check_subscriber_validity(self, config):
        for item in config:
            if (item['ros2Config']['messageType'] not in self.support_type_list['supportMessageTypes'][1]['subscriber']):
                raise Exception(f"Unsupported Message Type, {item['ros2Config']['messageType']}")
    


class PublisherMoraiSimSetup(Node):
    executor = None
    
    def __init__(self):
        super().__init__('morai_sim_ros2_configuration')
        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value
        QOS_RKL10TL = QoSProfile(
            reliability = QoSReliabilityPolicy.RELIABLE,
            history = QoSHistoryPolicy.KEEP_LAST,
            depth = qos_depth,
            durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.publisher_ = self.create_publisher(MoraiSimConfig,
                                                '/morai_sim_ros2_setup',
                                                QOS_RKL10TL)
        
    def publish_msg(self, morai_sim_config):
        print(morai_sim_config)
        msg = MoraiSimConfig()
        msg.publisher_list = json.JSONEncoder().encode(morai_sim_config['publisherList'][:])
        msg.subscriber_list = json.JSONEncoder().encode(morai_sim_config['subscriberList'][:])
        msg.service_list = json.JSONEncoder().encode(morai_sim_config['serviceList'][:])
        msg.sensor_config_file_name = json.JSONEncoder().encode(morai_sim_config['sensorConfigFileName'][:])
        msg.camera_list = json.JSONEncoder().encode(morai_sim_config['cameraList'][:])
        msg.gps_list = json.JSONEncoder().encode(morai_sim_config['GPSList'][:])
        msg.imu_list = json.JSONEncoder().encode(morai_sim_config['IMUList'][:])
        self.publisher_.publish(msg)
        
def main(args=None):
    global file_name
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    args = parser.parse_args()

    if (args.file != None):
        file_name = args.file
    config_loader = None
    morai_sim_config = None
    try:       
        config_loader = MoraiConfigFileHandler()
        config_loader.load_support_types()
        morai_sim_config = config_loader.load_config()
    except Exception as e:
        print(f'Error: {e}')
        exit(-1)
    
    rclpy.init()
    node = PublisherMoraiSimSetup()
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    try:
        while rclpy.ok():
            executor.spin_once(timeout_sec=1)
            node.publish_msg(morai_sim_config)
            break
    except Exception as e:
        print(f'Error: {e}')
    finally: 
        node.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()