# -*- coding: utf-8 -*-

from DateTime import DateTime

from plone import api
from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import (login,
                               TEST_USER_NAME,
                               setRoles,
                               TEST_USER_ID)

import ric.core


class RICCorePloneWithPackageLayer(PloneWithPackageLayer):
    """
    plone (portal root)
    |
    `-- 1: Annuaire        (directory)
        |-- 2: Affinitic   (organization)
        |   |-- 3: Tintin  (person)
        |   `-- 3: Haddock
        |
        `-- 2: Imio
            `-- 3: Dupont
    """

    products = ('collective.contact.membrane', 'Products.membrane')

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        self.loadZCML(package=ric.core,
                      name='testing.zcml')
        z2.installProduct(app, 'Products.membrane')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ric.core:testing')

        old_user_properties = {'last_login_time': DateTime(2000, 1, 1)}
        api.user.create(email='old_user@example.com',
                        username='old_user',
                        properties=old_user_properties)

        new_user_properties = {'last_login_time': DateTime()}
        api.user.create(email='new_user@example.com',
                        username='new_user',
                        properties=new_user_properties)

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        annuaire = api.content.create(
            type='directory',
            title='Annuaire',
            id='annuaire',
            container=portal)

        affinitic = api.content.create(
            type='organization',
            title='Affinitic',
            id='affinitic',
            subscriptions=[
                {'year': 2014,
                 'payment': False},
                {'year': 2013,
                 'payment': True}],
            email='info@affinitic.be',
            container=annuaire)
        api.content.create(
            type='person',
            title='Tintin',
            id='tintin',
            email='tintin@affinitic.be',
            container=affinitic)
        api.content.create(
            type='person',
            title='Haddock',
            id='haddock',
            email='haddock@affinitic.be',
            container=affinitic)

        imio = api.content.create(
            type='organization',
            title='Imio',
            id='imio',
            subscriptions=[
                {'year': 2014,
                 'payment': False},
                {'year': 2013,
                 'payment': False}],
            email='info@imio.be',
            container=annuaire)
        api.content.create(
            type='person',
            title='Dupont',
            id='dupont',
            email='dupont@imio.be',
            container=imio)


RIC_CORE_FIXTURE = RICCorePloneWithPackageLayer(
    name="RIC_CORE_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=ric.core,
    gs_profile_id="ric.core:testing")

RIC_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RIC_CORE_FIXTURE,),
    name="ric.core:Integration")

RIC_CORE_ROBOT_TESTING = FunctionalTesting(
    bases=(RIC_CORE_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ric.core:Robot")
