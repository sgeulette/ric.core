# -*- coding: utf-8 -*-

from mock import Mock

import unittest2 as unittest

from ric.core.mail.send_mail import SendMail
from ric.core.testing import RIC_CORE_INTEGRATION_TESTING


class TestMenu(unittest.TestCase):

    layer = RIC_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_update(self):
        send_mail = SendMail(self.portal, self.request)
        send_mail.send_mail = Mock(return_value=['recipient1'])
        send_mail.request.set('filter', 'foo')
        send_mail.update()

        from Products.statusmessages.interfaces import IStatusMessage
        self.assertEqual(len(IStatusMessage(self.request).show()), 1)

    def test_update_no_filter(self):
        send_mail = SendMail(self.portal, self.request)
        send_mail.send_mail = Mock(return_value=['recipient1'])
        send_mail.update()

        from Products.statusmessages.interfaces import IStatusMessage
        self.assertEqual(len(IStatusMessage(self.request).show()), 0)
