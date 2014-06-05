# -*- coding: utf-8 -*-
import plone.api
import logging


def UninstallGWT(context):
    """Not used"""
    if context.readDataFile('genweb.alternatheme_various.txt') is None:
        return

    logger = logging.getLogger(__name__)

    pqi = plone.api.portal.get_tool('portal_quickinstaller')
    pqi.uninstallProducts(['genweb.theme'])
    logger.warning('Uninstalled genweb.theme')
