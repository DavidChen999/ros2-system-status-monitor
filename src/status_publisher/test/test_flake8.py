# Copyright 2026 ROS 2 System Status Monitor contributors
# SPDX-License-Identifier: MIT

from ament_flake8.main import main


def test_flake8():
    assert main(argv=[".", "test"]) == 0
