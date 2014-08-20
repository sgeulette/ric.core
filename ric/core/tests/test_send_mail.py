# -*- coding: utf-8 -*-

from mock import Mock
from email import message_from_string

import unittest2 as unittest

from Acquisition import aq_base
from zope.component import getSiteManager
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
import transaction

from ric.core.mail.send_mail import SendMail
from ric.core.testing import RIC_CORE_INTEGRATION_TESTING

# See ticket 5907
import Products.membrane
# Pep8
Products.membrane


class TestSendMail(unittest.TestCase):

    layer = RIC_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self._setUpMail()

    def _setUpMail(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

        self.portal.email_from_address = 'noreply@holokinesislibros.com'
        transaction.commit()

    def tearDown(self):
        self.portal.MailHost = self.portal._original_MailHost
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(self.portal._original_MailHost),
                           provided=IMailHost)

    def test_update(self):
        """test update() method with filter specified"""
        send_mail = SendMail(self.portal, self.request)
        send_mail.send_mail = Mock(return_value=['recipient1@example.com'])
        send_mail.request.set('filter', 'foo')
        send_mail.update()

        from Products.statusmessages.interfaces import IStatusMessage
        self.assertEqual(len(IStatusMessage(self.request).show()), 1)

    def test_update_no_filter(self):
        """test update() method without filter specified"""
        send_mail = SendMail(self.portal, self.request)
        send_mail.send_mail = Mock(return_value=['recipient1@example.com'])
        send_mail.update()

        from Products.statusmessages.interfaces import IStatusMessage
        self.assertEqual(len(IStatusMessage(self.request).show()), 0)

    def test_send_mail_non_contributor(self):
        """test send_mail() method"""
        send_mail = SendMail(self.portal, self.request)
        send_mail.get_non_contributor_organizations = Mock(return_value=['non_contributor@example.com'])
        send_mail.request.set('option', '2014')
        recipients = send_mail.send_mail('non_contributor')
        self.assertEqual(recipients, ['non_contributor@example.com'])

        # Check if mail has been sent
        mailhost = self.portal.MailHost
        self.assertEqual(len(mailhost.messages), 1)
        msg = message_from_string(mailhost.messages[0])
        self.assertEqual(msg['To'], 'non_contributor@example.com')

#     def test_notify(self):
#         """test _notify() method"""
#         self.assertTrue(False)

#     def test_get_non_contributor_organization(self):
#         """test get_non_contributor_organizations() method"""
#         self.assertTrue(False)

#     def test_get_organization_members(self):
#         """test get_organization_members() method"""
#         self.assertTrue(False)

#     def test_get_non_connected_members(self):
#         """test get_non_connected_members() method"""
#         self.assertTrue(False)

#     def test_get_person_by_fields(self):
#         """test get_person_by_fields() method"""
#         self.assertTrue(False)

#     def test_get_multimail_fields(self):
#         """test get_multimail_fields() method"""
#         self.assertTrue(False)

#     def test_get_all_organizations(self):
#         """test get_all_organizations() method"""
#         self.assertTrue(False)

#     def test_convert_datetime(self):
#         """test convert_datetime() function"""
#         self.assertTrue(False)
