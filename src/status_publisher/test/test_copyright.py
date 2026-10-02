# Copyright 2026 ROS 2 System Status Monitor contributors
# SPDX-License-Identifier: MIT

from ament_copyright.main import main


def test_copyright():
    assert main(argv=[".", "test"]) == 0
