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
            "publish_multi_ego_setting = morai_sim_examples.publishers.pub_multi_ego_setting:main",
            "publish_skid_ctrl_cmd = morai_sim_examples.publishers.pub_skid_ctrl_cmd:main",
            "publish_set_traffic_light = morai_sim_examples.publishers.pub_set_traffic_light:main",
            "subscription_skid_ctrl_report = morai_sim_examples.subscribers.sub_skid_ctrl_report:main",
            "subscription_gps = morai_sim_examples.subscribers.sub_gps:main",
            "subscription_imu = morai_sim_examples.subscribers.sub_imu:main",
            "subscription_image = morai_sim_examples.subscribers.sub_camera_jpeg:main",
            "subscription_object_info = morai_sim_examples.subscribers.sub_object_info:main"
        ],
    },
)
