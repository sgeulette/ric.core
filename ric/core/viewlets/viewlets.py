from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CotisationViewlet(ViewletBase):
    render = ViewPageTemplateFile('cotisation.pt')

    def available(self):
        return True


class ProfileViewlet(ViewletBase):
    render = ViewPageTemplateFile('profile.pt')

    def available(self):
        return True
