#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-17 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.lcd.device import pcd8544
from luma.core.render import canvas

import baseline_data
from helpers import call, serial, setup_function  # noqa: F401


def test_init_84x48():
    pcd8544(serial)
    serial.command.assert_has_calls([
        call(33, 20, 176, 32),
        call(32, 128, 64),
        call(12)
    ])

    # Next 1024 are all data: zero's to clear the RAM
    # (1024 = 128 * 64 / 8)
    serial.data.assert_called_once_with([0] * (84 * 48 // 8))


def test_hide():
    device = pcd8544(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(8)


def test_show():
    device = pcd8544(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(12)


def test_display():
    device = pcd8544(serial)
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(32, 128, 64)

    # Next 1024 bytes are data representing the drawn image
    serial.data.assert_called_once_with(baseline_data.demo_pcd8544)
