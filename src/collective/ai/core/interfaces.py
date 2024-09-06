# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone.autoform.interfaces import IFormFieldProvider
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveAiCoreLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveAiControlPanelFieldProvider(IFormFieldProvider):
    pass
