# -*- coding: utf-8 -*-

from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

security = ModuleSecurityInfo('ric.core.permissions')

security.declarePublic('RICViewWarningViewlets')
RICViewWarningViewlets = 'RIC: View warning viewlets'
setDefaultRoles(RICViewWarningViewlets, ('Site Administrator', 'Member'))

security.declarePublic('RICAdministrator')
RICAdministrator = 'RIC: Administer website'
setDefaultRoles(RICAdministrator, ('Site Administrator', 'Manager'))
