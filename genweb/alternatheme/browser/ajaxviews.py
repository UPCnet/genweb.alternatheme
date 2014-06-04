# -*- coding: utf-8 -*-
from five import grok
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import ComponentLookupError
from zope.interface import providedBy
from zope.interface import Interface
from zope.i18n import translate
from plone.memoize.view import memoize_contextless
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage


def test(condition, value_true, value_false):
    if condition:
        return value_true
    else:
        return value_false


class AjaxBaseView(grok.View):
    grok.baseclass()

    hide = False
    __alias__ = None

    def test(self):
        return test

    @memoize_contextless
    def isAnon(self):
        return self.mtool().isAnonymousUser()

    @memoize_contextless
    def normalizeString(self):

        return getToolByName(self.context, 'plone_utils').normalizeString

    @memoize_contextless
    def mtool(self):

        plone_tools = getMultiAdapter((self.context, self.request),
                                      name=u'plone_tools')
        return plone_tools.membership()

    @memoize_contextless
    def portal_url(self):

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.portal_url()

    @memoize_contextless
    def site_properties(self):

        plone_tools = getMultiAdapter((self.context, self.request),
                                      name=u'plone_tools')
        return plone_tools.properties().site_properties

    @memoize_contextless
    def friendlyTypes(self):

        return getToolByName(self.context, 'plone_utils').getUserFriendlyTypes()


class folderSummaryView(AjaxBaseView):
    grok.name('ajax_folder_summary_view')
    grok.template('folder_summary_view')
    grok.context(Interface)
