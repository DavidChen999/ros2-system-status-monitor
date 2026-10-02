# Copyright 2026 ROS 2 System Status Monitor contributors
# SPDX-License-Identifier: MIT

import socket

import psutil
import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus


class SysStatusPub(Node):
    def __init__(self):
        super().__init__("sys_status_pub")
        self.publisher = self.create_publisher(
            SystemStatus, "system_status", 10
        )
        self.hostname = socket.gethostname()
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info("Publishing system status on /system_status")

    def publish_status(self):
        memory = psutil.virtual_memory()
        network = psutil.net_io_counters()

        status = SystemStatus()
        status.timestamp = self.get_clock().now().to_msg()
        status.hostname = self.hostname
        status.cpu_usage_percent = psutil.cpu_percent(interval=None)
        status.memory_usage_percent = memory.percent
        status.memory_total_bytes = memory.total
        status.memory_available_bytes = memory.available
        status.network_rx_bytes = network.bytes_recv
        status.network_tx_bytes = network.bytes_sent
        self.publisher.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = SysStatusPub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
