# Copyright 2026 ROS 2 System Status Monitor contributors
# SPDX-License-Identifier: MIT

import sys
from datetime import datetime

import rclpy
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from rclpy.node import Node
from status_interfaces.msg import SystemStatus


def format_bytes(value):
    size = float(value)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024.0 or unit == "TiB":
            return f"{size:.1f} {unit}"
        size /= 1024.0


class SysStatusGui(Node):
    def __init__(self):
        super().__init__("sys_status_gui")
        self.window = QWidget()
        self.window.setWindowTitle("ROS 2 系统状态监视器")
        self.window.setMinimumWidth(360)

        layout = QVBoxLayout(self.window)
        self.labels = {
            key: QLabel(f"{title}: 等待状态数据...")
            for key, title in (
                ("timestamp", "记录时间"),
                ("hostname", "主机名"),
                ("cpu", "CPU 使用率"),
                ("memory", "内存使用率"),
                ("memory_size", "内存总量 / 剩余可用"),
                ("network_rx", "网络累计接收"),
                ("network_tx", "网络累计发送"),
            )
        }
        for label in self.labels.values():
            layout.addWidget(label)

        self.subscription = self.create_subscription(
            SystemStatus, "system_status", self.update_status, 10
        )

    def update_status(self, status):
        timestamp = datetime.fromtimestamp(
            status.timestamp.sec + status.timestamp.nanosec / 1_000_000_000
        ).astimezone()
        self.labels["timestamp"].setText(
            f"记录时间: {timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )
        self.labels["hostname"].setText(f"主机名: {status.hostname}")
        self.labels["cpu"].setText(
            f"CPU 使用率: {status.cpu_usage_percent:.1f}%"
        )
        self.labels["memory"].setText(
            f"内存使用率: {status.memory_usage_percent:.1f}%"
        )
        self.labels["memory_size"].setText(
            "内存总量 / 剩余可用: "
            f"{format_bytes(status.memory_total_bytes)} / "
            f"{format_bytes(status.memory_available_bytes)}"
        )
        self.labels["network_rx"].setText(
            f"网络累计接收: {format_bytes(status.network_rx_bytes)}"
        )
        self.labels["network_tx"].setText(
            f"网络累计发送: {format_bytes(status.network_tx_bytes)}"
        )


def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    node = SysStatusGui()

    ros_timer = QTimer()
    ros_timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0))
    ros_timer.start(50)
    app.aboutToQuit.connect(node.destroy_node)
    app.aboutToQuit.connect(lambda: rclpy.shutdown() if rclpy.ok() else None)
    node.window.show()

    try:
        app.exec_()
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
