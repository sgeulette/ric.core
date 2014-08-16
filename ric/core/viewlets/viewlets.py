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

    def available(self):
        return False


class ProfileViewlet(RICViewletBase):
    render = ViewPageTemplateFile('profile.pt')

    def available(self):
        return False


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
