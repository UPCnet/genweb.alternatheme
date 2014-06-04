import unittest2 as unittest

from plone.testing.z2 import Browser

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles

from genweb.alternatheme.testing import GENWEBTHEME_INTEGRATION_TESTING
from genweb.alternatheme.testing import GENWEBTHEME_FUNCTIONAL_TESTING

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from zope.component import getUtility, getMultiAdapter


class BasicTest(unittest.TestCase):

    layer = GENWEBTHEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.app = self.layer['app']

    def test_genweb_layers_available(self):
        self.failUnless('genwebtheme_custom' in self.portal.portal_skins)

    def test_genweb_skin_installed(self):
        self.skins = self.portal.portal_skins
        theme = self.skins.getDefaultSkin()
        self.failUnless(theme == 'GenwebTheme', 'Default theme is %s' % theme)


class BootstrapTraversalTest(unittest.TestCase):

    layer = GENWEBTHEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.app = self.layer['app']
        self.browser = Browser(self.app)

    def testGWResourceTraversal(self):
        portalURL = self.portal.absolute_url()
        self.browser.open('%s/++gw++stylesheets/genwebupc.css' % portalURL)
        self.assertTrue("Bootstrap" in self.browser.contents)
