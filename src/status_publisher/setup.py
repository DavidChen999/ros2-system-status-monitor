# Copyright 2026 ROS 2 System Status Monitor contributors
# SPDX-License-Identifier: MIT

from setuptools import find_packages, setup

package_name = "status_publisher"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ROS 2 System Status Monitor contributors",
    maintainer_email="maintainer@example.com",
    description="Publishes system metrics and displays them in a Qt window.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "sys_status_pub = status_publisher.sys_status_pub:main",
            "sys_status_gui = status_publisher.sys_status_gui:main",
        ],
    },
)
