from Acquisition import aq_parent, aq_inner
from plone import memoize
from plone.app.contentmenu.interfaces import IActionsMenu, IActionsSubMenuItem
from plone.protect.utils import addTokenToUrl
from zope.browsermenu.interfaces import IBrowserSubMenuItem, IBrowserMenu
from zope.browsermenu.menu import BrowserMenu, BrowserSubMenuItem
from zope.component import getMultiAdapter, queryUtility, getAllUtilitiesRegisteredFor
from zope.interface import implementer
from collective.ai.core.interfaces import IAiActionsProvider
from collective.ai.core import _

class IAiActionsMenu(IBrowserMenu):
    """The menu item linking to the actions menu."""


@implementer(IActionsSubMenuItem)
class AiActionsSubMenuItem(BrowserSubMenuItem):
    title = _("collective_ai_actions", default="Actions")
    description = _(
        "title_actions_menu", default="Actions for the current content item"
    )
    submenuId = "collective-ai-actions"
    icon = "stars"
    order = 60
    extra = {
        "id": "plone-contentmenu-actions",
        "li_class": "plonetoolbar-content-action",
    }

    def __init__(self, context, request):
        super().__init__(context, request)
        self.context_state = getMultiAdapter(
            (context, request), name="plone_context_state"
        )

    @property
    def action(self):
        folder = self.context
        if not self.context_state.is_structural_folder():
            folder = aq_parent(aq_inner(self.context))
        return folder.absolute_url() + "/folder_contents"

    def available(self):
        return True

    def selected(self):
        return False


@implementer(IAiActionsMenu)
class AiActionsMenu(BrowserMenu):
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []
        context_state = getMultiAdapter((context, request), name="plone_context_state")
        ai_actions = context_state.actions("ai_actions")
        for action in ai_actions:
            if not action["allowed"]:
                continue
            aid = action["id"]
            cssClass = f"actionicon-object_buttons-{aid}"
            icon = action.get("icon", None)
            modal = action.get("modal", None)
            if modal:
                cssClass += " pat-plone-modal"

            results.append(
                {
                    "title": action["title"],
                    "description": action.get("description", ""),
                    "action": addTokenToUrl(action["url"], request),
                    "selected": False,
                    "icon": icon,
                    "extra": {
                        "id": "plone-contentmenu-actions-" + aid,
                        "separator": None,
                        "class": cssClass,
                        "modal": modal,
                    },
                    "submenu": None,
                }
            )

        addon_actions_providers = getAllUtilitiesRegisteredFor(IAiActionsProvider)
        for actions_provider in addon_actions_providers:
            for action in actions_provider(context, request):
                results.append(action)
        return results
