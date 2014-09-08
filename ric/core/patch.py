# -*- coding: utf-8 -*-
from Products.membrane.interfaces import user as user_ifaces


def getUserObject(self, login=None, user_id=None, brain=False):
    """
    Return the authentication implementation (content item) for a
    given login or userid.
    """
    query = {}
    if user_id:
        if self.case_sensitive_auth and \
               ('exact_getUserId' in self._catalog.indexes):
            query["exact_getUserId"] = user_id
        else:
            query["getUserId"] = user_id
    elif login:
        if self.case_sensitive_auth and \
               ('exact_getUserName' in self._catalog.indexes):
            query["exact_getUserName"] = login
        else:
            query["getUserName"] = login

    if not query:  # No user_id or login name given
        return None

    query["object_implements"
          ] = user_ifaces.IMembraneUserAuth.__identifier__
    uSR = self.unrestrictedSearchResults
    members = uSR(**query)

    # filter out inadvertent ZCTextIndex matches by only keeping
    # records with the same number of characters
    if "getUserName" in query:
        members = [mem for mem in members
                   if len(mem.getUserName) == len(login)]
    if "getUserId" in query:
        members = [mem for mem in members
                   if len(mem.getUserId) == len(user_id)]

    if not members:
        return None

    if brain:
        return members[0]

    member = members[0]._unrestrictedGetObject()
    return member
