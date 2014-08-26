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
        send_mail.get_non_contributor_organizations_members = Mock(return_value=members)
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
        members = send_mail.get_non_contributor_organizations_members(2014)
        self.assertEqual(len(members), 3)
        self.assertTrue('tintin@affinitic.be' in members)
        self.assertTrue('haddock@affinitic.be' in members)
        self.assertTrue('dupont@imio.be' in members)

        members = send_mail.get_non_contributor_organizations_members(2013)
        self.assertEqual(len(members), 1)
        self.assertTrue('dupont@imio.be' in members)

        members = send_mail.get_non_contributor_organizations_members(2015)
        self.assertEqual(len(members), 0)

    def test_get_organization_members(self):
        """test get_organization_members() method"""
        send_mail = SendMail(self.portal, self.request)
        members = send_mail.get_organization_members('affinitic')
        self.assertEqual(len(members), 2)
        self.assertTrue('tintin@affinitic.be' in members)
        self.assertTrue('haddock@affinitic.be' in members)

        members = send_mail.get_organization_members('imio')
        self.assertEqual(len(members), 1)
        self.assertTrue('dupont@imio.be' in members)

    def test_get_non_connected_members(self):
        """test get_non_connected_members() method"""
        send_mail = SendMail(self.portal, self.request)
        members = send_mail.get_non_connected_members(265)
        self.assertTrue('old_user@example.com' in members)
        self.assertTrue('new_user@example.com' not in members)

    def test_get_person_by_fields(self):
        """test get_person_by_fields() method"""
        send_mail = SendMail(self.portal, self.request)
        members = send_mail.get_person_by_fields(['contact_cotisation', 'formation'])
        self.assertEqual(len(members), 2)
        self.assertTrue('tintin@affinitic.be' in members)
        self.assertTrue('dupont@imio.be' in members)

        members = send_mail.get_person_by_fields(['contact_cotisation'])
        self.assertEqual(len(members), 1)
        self.assertTrue('tintin@affinitic.be' in members)

        members = send_mail.get_person_by_fields(['formation'])
        self.assertEqual(len(members), 2)
        self.assertTrue('tintin@affinitic.be' in members)
        self.assertTrue('dupont@imio.be' in members)

        members = send_mail.get_person_by_fields(['notexists'])
        self.assertEqual(len(members), 0)

    def test_get_multimail_fields(self):
        """test get_multimail_fields() method"""
        send_mail = SendMail(self.portal, self.request)
        fields = send_mail.get_multimail_fields()
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields,
                         [(u'contact_cotisation', u'contact_cotisation'),
                          (u'formation', u'formation')])

    def test_get_all_organizations(self):
        """test get_all_organizations() method"""
        send_mail = SendMail(self.portal, self.request)
        organizations = send_mail.get_all_organizations()
        self.assertEqual(len(organizations), 2)
        ids = [org.id for org in organizations]
        self.assertTrue('affinitic' in ids)
        self.assertTrue('imio' in ids)

    def test_convert_datetime(self):
        """test convert_datetime() function"""
        from ric.core.mail.send_mail import convert_datetime
        from DateTime import DateTime
        from datetime import datetime
        zope_dt = DateTime(2010, 6, 20, 11, 45, 55)
        python_dt = convert_datetime(zope_dt)
        self.assertEqual(python_dt, datetime(2010, 6, 20, 11, 45, 55))
