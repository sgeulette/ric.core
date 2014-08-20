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
        """test send_mail() for non contributors method"""
        send_mail = SendMail(self.portal, self.request)
        members = ['non_contributor@example.com']
        send_mail.get_non_contributor_organizations = Mock(return_value=members)
        send_mail.request.set('option', '2014')
        recipients = send_mail.send_mail('non_contributor')
        self.assertEqual(recipients, members)

        # Check if mail has been sent
        mailhost = self.portal.MailHost
        self.assertEqual(len(mailhost.messages), 1)
        msg = message_from_string(mailhost.messages[0])
        self.assertEqual(msg['To'], members[0])

    def test_send_mail_organization_members(self):
        """test send_mail() for organization members method"""
        send_mail = SendMail(self.portal, self.request)
        members = ['organization_member1@example.com',
                   'organization_member2@example.com']
        send_mail.get_organization_members = Mock(return_value=members)
        send_mail.request.set('option', 'organization')
        recipients = send_mail.send_mail('organization_members')
        self.assertEqual(recipients, members)

        # Check if mail has been sent
        mailhost = self.portal.MailHost
        self.assertEqual(len(mailhost.messages), 2)
        msg = message_from_string(mailhost.messages[0])
        self.assertEqual(msg['To'], members[0])
        msg = message_from_string(mailhost.messages[1])
        self.assertEqual(msg['To'], members[1])

    def test_send_mail_non_connected_members(self):
        """test send_mail() for non connected members method"""
        send_mail = SendMail(self.portal, self.request)
        members = ['non_connected_member@example.com']
        send_mail.get_non_connected_members = Mock(return_value=members)
        send_mail.request.set('option', '10')
        recipients = send_mail.send_mail('non_connected_members')
        self.assertEqual(recipients, members)

        # Check if mail has been sent
        mailhost = self.portal.MailHost
        self.assertEqual(len(mailhost.messages), 1)
        msg = message_from_string(mailhost.messages[0])
        self.assertEqual(msg['To'], members[0])

    def test_send_mail_send_mail_field(self):
        """test send_mail() for send mail fields method"""
        send_mail = SendMail(self.portal, self.request)
        members = ['mail_field@example.com']
        send_mail.get_person_by_fields = Mock(return_value=members)
        send_mail.request.set('option', ['field1', 'field2'])
        recipients = send_mail.send_mail('send_mail_field')
        self.assertEqual(recipients, members)

        # Check if mail has been sent
        mailhost = self.portal.MailHost
        self.assertEqual(len(mailhost.messages), 1)
        msg = message_from_string(mailhost.messages[0])
        self.assertEqual(msg['To'], members[0])

    def test_get_non_contributor_organization(self):
        """test get_non_contributor_organizations() method"""
        send_mail = SendMail(self.portal, self.request)
        organizations = send_mail.get_non_contributor_organizations(2014)
        self.assertEqual(len(organizations), 2)
        self.assertTrue('info@affinitic.be' in organizations)
        self.assertTrue('info@imio.be' in organizations)

        organizations = send_mail.get_non_contributor_organizations(2013)
        self.assertEqual(len(organizations), 1)
        self.assertTrue('info@imio.be' in organizations)

        organizations = send_mail.get_non_contributor_organizations(2015)
        self.assertEqual(len(organizations), 0)


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
