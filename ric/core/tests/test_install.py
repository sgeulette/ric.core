# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.uuid.interfaces import IUUID
from ric.core.testing import RIC_CORE_INTEGRATION_TESTING


class TestInstall(unittest.TestCase):

    layer = RIC_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_plonesite_uuid(self):
        self.assertTrue(IUUID(self.portal) is not None)
