# -*- coding: utf-8 -*-
from Products.CMFCore.ActionInformation import ActionInfo
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.ai.summarizer import _
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.schema import JSONField
from plone.z3cform import layout
from zope import schema
from zope.component import queryAdapter
from zope.interface import Interface, implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

class IAITextCompletionService(Interface):
    label = schema.TextLine(
        title=_("Label"),
        required=True,
    )
    service_type = schema.Choice(
        title=_("Service type"),
        vocabulary="collective.ai.core.vocabularies.ServiceTypesVocabulary",
        required=True,
    )
    api_service_url = schema.URI(
        title=_("Service URL"),
        required=False,
    )
    api_key = schema.TextLine(
        title=_("API key"),
        required=False,
    )
    extra_config = JSONField(
        title=_("Extra Configuration (JSON)"),
        description=_("Additional configuration in JSON format for this service."),
        required=False,
    )
    active = schema.Bool(
        title=_("Active"),
        required=False,
        default=True,
    )


class IAICoreSettings(Interface):
    directives.widget('ai_text_completion_services',
                      BlockDataGridFieldFactory,
                      allow_reorder=False,
                      auto_append=False)
    ai_text_completion_services = schema.List(
        title=_("AI text completion services"),
        value_type=DictRow(
            title=_("AI text completion service"),
            schema=IAITextCompletionService,
        ),
        required=False,
    )

class AICoreControlPanelForm(RegistryEditForm):
    label = _("Main AI settings")
    schema = IAICoreSettings

class AICoreControlPanelFormWrapper(ControlPanelFormWrapper):
    index = ViewPageTemplateFile("controlpanel_layout.pt")

    def __init__(self, context, request):
        super().__init__(context, request)
        self.tabs = self.get_ai_controlpanel_tabs()
        self.active_tab = self.get_active_tab()


    def get_ai_controlpanel_tabs(self):
        portal_actions = api.portal.get_tool('portal_actions')
        actions = portal_actions.listActions(categories=['ai_controlpanel_tabs'])
        ec = portal_actions._getExprContext(self.context)
        actions = [ActionInfo(action, ec) for action in actions]
        return actions

    def get_active_tab(self):
        return next(filter(lambda x: x['url'].split('/')[-1] == self.request.getURL().split('/')[-1], self.tabs))

AiCoreControlPanelView = layout.wrap_form(AICoreControlPanelForm, AICoreControlPanelFormWrapper)
