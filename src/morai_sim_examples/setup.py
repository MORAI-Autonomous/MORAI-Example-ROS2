from setuptools import setup

package_name = 'morai_sim_examples'
clients = 'morai_sim_examples/clients/'
publishers = 'morai_sim_examples/publishers/'
subscribers = 'morai_sim_examples/subscribers/'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, clients, publishers, subscribers],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='MORAI',
    maintainer_email='shpark@morai.ai',
    description='MORAI SIM: Robotics ROS2 examples',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "client_event_cmd = morai_sim_examples.clients.morai_client_event_cmd:main",
            "publish_ctrl_cmd = morai_sim_examples.publishers.pub_ctrl_cmd:main",
            "publish_intsn_control = morai_sim_examples.publishers.pub_intsn_control:main",
            "publish_multi_ego_setting = morai_sim_examples.publishers.pub_multi_ego_setting:main",
            "publish_set_traffic_light = morai_sim_examples.publishers.pub_set_traffic_light:main",
            "subscription_camera_jpeg = morai_sim_examples.subscribers.sub_camera_jpeg:main",
            "subscription_ego_vehicle_status = morai_sim_examples.subscribers.sub_ego_vehicle_status:main",
            "subscription_gps = morai_sim_examples.subscribers.sub_gps:main",
            "subscription_imu = morai_sim_examples.subscribers.sub_imu:main",
            "subscription_intersection_status = morai_sim_examples.subscribers.sub_intersection_status:main",
            "subscription_object_info = morai_sim_examples.subscribers.sub_object_info:main",
            "subscription_traffic_light_status = morai_sim_examples.subscribers.sub_traffic_light_status:main"
        ],
    },
)
