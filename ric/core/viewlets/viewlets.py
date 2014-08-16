from plone import api
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class RICViewletBase(ViewletBase):
    """
    """

    def available():
        pass


class CotisationViewlet(RICViewletBase):
    render = ViewPageTemplateFile('cotisation.pt')
    organizationlink = ""

    def available(self):
        organization = getMultiAdapter((self.context, self.request),
                                       name="get_organization_for_user")()
        contactCotisation = False
        if organization:
            catalog = api.portal.get_tool('portal_catalog')
            persons = catalog.searchResults(portal_type="person",
                                            path={'query': '/'.join(organization.getPhysicalPath()),
                                                  'depth': 1})
            for person in persons:
                personObj = person.getObject()
                if 'contact cotisation' in personObj.multimail:
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

    def available(self):
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
