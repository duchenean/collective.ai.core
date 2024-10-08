from collective.ai.core.browser.controlpanel import IAiCoreSettings, IAiTextCompletionService
from plone.base.interfaces import IEditingSchema
from plone.registry.interfaces import IRegistry
from zope.component import getUtility, queryAdapter, getAdapters
from zope.interface import provider, implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.ai.core.services import IAiAPIService
from collective.ai.core import _


@implementer(IVocabularyFactory)
class ServiceTypesVocabulary:
    def __call__(self, context):
        factories = getAdapters((IAiTextCompletionService,), IAiAPIService)
        terms = [
            SimpleTerm(f[0], f[0], getattr(f[1], "name", f[0])) for f in factories
        ]
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class ActiveTextCompletionServicesVocabulary:
    def __call__(self, context):
        registry = getUtility(IRegistry)
        ai_settings = registry.forInterface(IAiCoreSettings, check=False)
        terms = [
            SimpleTerm(i, s['label'], s['label']) for i,s in enumerate(ai_settings.ai_text_completion_services)
            if s['active']
        ]
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class TextCompletionServicesVocabulary:
    def __call__(self, context):
        registry = getUtility(IRegistry)
        ai_settings = registry.forInterface(IAiCoreSettings, check=False)
        terms = [
            SimpleTerm(i, s['label'], s['label']) for i,s in enumerate(ai_settings.ai_text_completion_services)
        ]
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class TextCompletionModelsVocabulary:
    def __call__(self, context):
        terms = []
        registry = getUtility(IRegistry)
        ai_settings = registry.forInterface(IAiCoreSettings, check=False)
        for i, s in enumerate(ai_settings.ai_text_completion_services):
            conn = queryAdapter(context, IAiAPIService, name=s['service_type'])
            if not conn:
                continue
            conn(i)
            models = conn.list_models()
            for model in models:
                id = f"{i}__{model}"
                label = s['label'] + " - " + model
                term = SimpleTerm(id, label, label)
                terms.append(term)

        return SimpleVocabulary(terms)
