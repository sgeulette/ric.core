# -*- coding: utf-8 -*-

from plone.testing import z2
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import ric.core


class RICCorePloneWithPackageLayer(PloneWithPackageLayer):
    """
    """

    def setUpPloneSite(self, portal):
        pass


RIC_CORE_FIXTURE = RICCorePloneWithPackageLayer(
    name="RIC_CORE_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=ric.core)

RIC_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RIC_CORE_FIXTURE,),
    name="ric.core:Integration")

RIC_CORE_ROBOT_TESTING = FunctionalTesting(
    bases=(RIC_CORE_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ric.core:Robot")