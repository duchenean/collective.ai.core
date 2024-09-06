from plone.api.portal import get_registry_record
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
class ServicesVocabulary(object):
    """Vocabulary factory for http protocols"""

    def __call__(self, context):
        return SimpleVocabulary(
            [
            ]
        )

