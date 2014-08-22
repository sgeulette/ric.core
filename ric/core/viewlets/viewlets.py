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
        organization = getMultiAdapter((self.context, self.request),
                                       name="get_organization_for_user")()
        if not organization:
            return False
        catalog = api.portal.get_tool('portal_catalog')
        persons = catalog.searchResults(portal_type="person",
                                        path={'query': '/'.join(organization.getPhysicalPath()),
                                              'depth': 1})
        contactCotisation = False
        for person in persons:
            personObj = person.getObject()
            if 'contact_cotisation' in personObj.multimail:
                contactCotisation = True
                break
        if not contactCotisation:
            self.organizationlink = organization.absolute_url()
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
                                 name="get_person_for_user")()
        if person:
            isCompleted = getMultiAdapter((person, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.personlink = person.absolute_url()
        organization = getMultiAdapter((self.context, self.request),
                                       name="get_organization_for_user")()
        if organization:
            isCompleted = getMultiAdapter((organization, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.organizationlink = organization.absolute_url()
        return bool(self.personlink or self.organizationlink)


class EmailViewlet(RICViewletBase):
    render = ViewPageTemplateFile('email.pt')
    link = ""

    def available(self):
        person = getMultiAdapter((self.context, self.request),
                                 name="get_person_for_user")()
        if person and person.invalidmail == True:
            self.link = person.absolute_url()
            return True
        return False
