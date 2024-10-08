from collective.ai.core.browser.controlpanel import IAiCoreSettings, IAiTextCompletionService
from plone.registry.interfaces import IRegistry
from zope.component import getUtility, adapter
from zope.interface import Interface, implementer
from openai import OpenAI


class IAiAPIService(Interface):

    def list_models(self):
        pass

    def complete(self, prompt):
        pass


@adapter(Interface, Interface)
@implementer(IAiAPIService)
class OpenAIService:
    name = "OpenAI"

    def __init__(self, context):
        registry = getUtility(IRegistry)
        self.ai_settings = registry.forInterface(IAiCoreSettings, check=False)

    def __call__(self, config_row):
        self.service_settings = self.ai_settings.ai_text_completion_services[config_row]
        extra_config = self.service_settings["extra_config"] or {}
        self.client = OpenAI(
            base_url=self.service_settings["api_service_url"],
            api_key=self.service_settings["api_key"],
            **extra_config
        )

    def complete(self, prompt):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def list_models(self):
        # models = self.client.models.list()
        # return [m.id for m in models.data]
        return ["gpt-4o-mini",]


@adapter(IAiTextCompletionService)
@implementer(IAiAPIService)
class MistralAIService(OpenAIService):
    name = "Mistral AI"

    def list_models(self):
        return [
            "mistral-large-latest",
            "open-mistral-nemo",
            "codestral-latest",
            "open-mistral-7b",
            "open-mixtral-8x7b",
            "open-mixtral-8x22b",
            "open-codestral-mamba"
        ]
