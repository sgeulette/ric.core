# -*- coding: utf-8 -*-
from plone.testing import layered
from ric.core.testing import RIC_CORE_ROBOT_TESTING

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('robot'),
                layer=RIC_CORE_ROBOT_TESTING),
    ])
    return suite
