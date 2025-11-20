from setuptools import setup

package_name = 'morai_ros2_connector'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shpark',
    maintainer_email='shpark@morai.ai',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'morai_sim_ros2_connector = morai_ros2_connector.morai_sim_ros2_connector:main'
        ],
    },
)
