from collective.ai.core.browser.controlpanel import IAICoreSettings, IAITextCompletionService
from plone.registry.interfaces import IRegistry
from zope.component import getUtility, adapter
from zope.interface import Interface, implementer
from openai import OpenAI


class IAIAPIService(Interface):

    def list_models(self):
        pass

    def complete(self, prompt):
        pass


@adapter(Interface)
@implementer(IAIAPIService)
class OpenAIService:
    name = "OpenAI"

    def __init__(self, context):
        registry = getUtility(IRegistry)
        self.ai_settings = registry.forInterface(IAICoreSettings, check=False)

    def __call__(self, config_row, model):
        self.service_settings = self.ai_settings.ai_text_completion_services[config_row]
        extra_config = self.service_settings["extra_config"] or {}
        self.client = OpenAI(
            base_url=self.service_settings["api_service_url"],
            api_key=self.service_settings["api_key"],
            **extra_config
        )
        self.model = model

    def complete(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def list_models(self):
        # models = self.client.models.list()
        # return [m.id for m in models.data]
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]


@adapter(Interface)
@implementer(IAIAPIService)
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


@adapter(Interface)
@implementer(IAIAPIService)
class OpenRouterAIService(OpenAIService):
    name = "OpenRouter"

    def list_models(self):
        return [
            "google/gemini-flash-1.5",
            "anthropic/claude-3.5-sonnet:beta",
            "meta-llama/llama-3.1-70b-instruct"
        ]
