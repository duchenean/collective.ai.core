# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.ai.core.testing import COLLECTIVE_AI_CORE_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.ai.core is properly installed."""

    layer = COLLECTIVE_AI_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.ai.core is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'collective.ai.core'))

    def test_browserlayer(self):
        """Test that ICollectiveAiCoreLayer is registered."""
        from collective.ai.core.interfaces import (
            ICollectiveAiCoreLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveAiCoreLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_AI_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('collective.ai.core')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.ai.core is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'collective.ai.core'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveAiCoreLayer is removed."""
        from collective.ai.core.interfaces import \
            ICollectiveAiCoreLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveAiCoreLayer, utils.registered_layers())
