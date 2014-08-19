# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleVocabulary as SV

from ric.core import RICMessageFactory as _


multimail = SV([
    SV.createTerm('contact_cotisation', 0, _(u'Contact cotisation')),
    SV.createTerm('formation', 1, _(u'Formation'))])
