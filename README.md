# ROS 2 System Status Monitor

Ubuntu 22.04 and ROS 2 Humble system status monitor. The workspace contains
two ROS 2 packages:

- `status_interfaces`: defines the `SystemStatus` message.
- `status_publisher`: publishes host metrics and provides a PyQt5 subscriber
  window.

The message includes the record timestamp, hostname, CPU and memory usage
percentages, total and available memory, and cumulative network bytes received
and sent since boot.

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- `python3-psutil`
- `python3-pyqt5`

Install the Python dependencies if they are not already available:

```bash
sudo apt update
sudo apt install python3-psutil python3-pyqt5
```

## Build

From the repository root, with ROS 2 Humble installed:

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Run

In one terminal, start the publisher:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run status_publisher sys_status_pub
```

In another terminal on the same ROS 2 domain, open the Qt window:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run status_publisher sys_status_gui
```

The publisher emits a `status_interfaces/msg/SystemStatus` message on
`/system_status` once per second. Network values are cumulative byte counters,
not instantaneous throughput.

## License

MIT
