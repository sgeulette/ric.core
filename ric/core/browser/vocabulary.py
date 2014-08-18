# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IBaseVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from ric.core import RICMessageFactory as _


CONTENTS = {'organization': _('Une organisation'),
            'person': _('Une personne')}


class Contents(object):
    """
    Vocabulary of contents to search on
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [SimpleTerm(key, key, item) for key, item in\
                 CONTENTS.items()]
        return SimpleVocabulary(items)

ContentsVocabularyFactory = Contents()
