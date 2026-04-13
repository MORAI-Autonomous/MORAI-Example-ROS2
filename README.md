# MORAI Example ROS2

Check that your MORAI SIM is configured correctly for communicating over ROS2 with this open-source example project

## File structure
```
./
├── release
│    └── morai_ros2_bridge_<version>  # bridge script to connect MORAI SIM with ROS2
└── src          
     ├── morai_ros2_connector         # script for MORAI Simulator to open ROS2 service
     ├── morai_ros2_msgs              # MORAI Simulator ROS2 message set (submodule)
     └── morai_sim_examples           # example ros2 nodes and unit testing code
```

## Dependencies

- **Notice**: we will be slowly phasing out support for sunsetted versions of ROS2 such as Eloquent and Foxy.

| ROS 2 Version | Supported | Ubuntu | Python |
|---|---|---|---|
| Eloquent | 🟢 | 18.04 | 3.6 |
| Foxy | 🟢 | 20.04 | 3.8 |
| Galactic | 🟢 | 20.04 | 3.8 |
| Humble | 🟢 (Updated 2025.12) | 22.04 | 3.10 |
| Iron | Not supported | 22.04 | 3.10 |
| Jazzy | 🟢 (Updated 2026.1) | 24.04 | 3.12 |
| Kilted | Not supported | 24.04 | 3.12 |

- The bridge scripts will remain fixed to each version, but the example codebase will adopt whichever version is the most recent. (i.e. if Humble is the most recent supported version, all source code will be tested on Humble only)
- Ubuntu version should match the ROS 2 distro (e.g. Humble --> Ubuntu 22.04)
- Python version should also match the ROS 2 distro (e.g. Humble would by default match with Python 3.10)

### Dependencies with MORAI SIM

This example repository is compatible up to MORAI SIM 24.R2.H2.

With the release of 26.R1., ROS2 Humble is natively supported by the simulator, no longer requiring the `morai_ros2_connector` script to connect to the ROS2 network.

## Setup

Build a ROS2 workspace with the ROS2 distro/version you are using.

```bash
$ mkdir ~/ws_morai_sim_example
$ cd ~/ws_morai_sim_example
$ git clone https://github.com/MORAI-Autonomous/MORAI-Example-ROS2.git
$ source /opt/ros/<your ROS2 version>/setup.bash
$ colcon build
$ source /install/setup.bash
```

## Use

Connecting MORAI SIM to ROS2 nodes is a two step process.

**Step 1**: Start the bridge executable

```bash
$ source /install/setup.bash
$ ./morai_ros2_bridge_<your ROS2 version>
```

If successful, the terminal should show: `MORAI Bridge: <version>`, followed by connection information.

**Step 2**: Run the connector python script

```bash
$ pip install -e src/morai_ros2_connector/
$ python3 src/morai_ros2_connector/morai_ros2_connector/morai_sim_ros2_connector.py
```

## Troubleshooting

Library dependencies can lead to the bridge executable failing to correctly start. Some libraries that may not be part of a standard wsl install that may need to manually installed are:
- libabsl-dev
- libgrpc++-dev

## Resources

- [Website](https://www.morai.ai/)
- **Documentation**:
  - [MORAI SIM Manual (English)](https://morai-sim-drive-user-manual-en-24-r2.scrollhelp.site/morai-sim-drive-user-manual-en-24.r2/Working-version/?l=en)
  - [MORAI SIM Manual (Korean)](https://help-morai-sim.scrollhelp.site/)

## License and acknowledgements

This project is licensed under the [MIT License](LICENSE).
