from AccessControl import getSecurityManager
from plone import api
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class RICViewletBase(ViewletBase):

    def viewletsToShowTomanager(self):
        context = self.context
        if context.portal_type not in ['organization', 'person']:
            return None
        sm = getSecurityManager()
        if sm.checkPermission('RIC: Administer website', context):
            return context.portal_type
        return None


class CotisationViewlet(RICViewletBase):
    render = ViewPageTemplateFile('cotisation.pt')
    organizationlink = ""
    isManager = False

    def available(self):
        if self.viewletsToShowTomanager() == 'organization':
            self.organizationlink = self.context.absolute_url()
            self.isManager = True
            return True
        organizations = getMultiAdapter((self.context, self.request),
                                       name="get_organizations_for_user")()
        if not organizations:
            return False
        catalog = api.portal.get_tool('portal_catalog')
        persons = catalog.searchResults(portal_type="person",
                                        path={'query': '/'.join(organizations.getPhysicalPath()),
                                              'depth': 1})
        contactCotisation = False
        for person in persons:
            personObj = person.getObject()
            if 'contact_cotisation' in personObj.multimail:
                contactCotisation = True
                break
        if not contactCotisation:
            self.organizationlink = organizations.absolute_url()
            return True
        return False


class ProfileViewlet(RICViewletBase):
    render = ViewPageTemplateFile('profile.pt')
    personlink = ""
    organizationlink = ""
    isManager = False

    def available(self):
        if self.viewletsToShowTomanager() == 'organization':
            self.organizationlink = self.context.absolute_url()
            self.isManager = True
            return True
        elif self.viewletsToShowTomanager() == 'person':
            self.personlink = self.context.absolute_url()
            self.isManager = True
            return True
        person = getMultiAdapter((self.context, self.request),
                                 name="get_persons_for_user")()
        if person:
            isCompleted = getMultiAdapter((person, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.personlink = person.absolute_url()
        organizations = getMultiAdapter((self.context, self.request),
                                       name="get_organizations_for_user")()
        if organizations:
            isCompleted = getMultiAdapter((organizations, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.organizationlink = organizations.absolute_url()
        return bool(self.personlink or self.organizationlink)


class EmailViewlet(RICViewletBase):
    render = ViewPageTemplateFile('email.pt')
    linksInfos = {}

    def available(self):
        persons = getMultiAdapter((self.context, self.request),
                                 name="get_persons_for_user")()
        if not persons:
            return False
        for person in persons:
            if person.invalidmail:
                self.linksInfos[person.absolute_url()] = person.Title()
        return bool(self.linksInfos)
