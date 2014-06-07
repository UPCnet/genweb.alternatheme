from Products.CMFCore.utils import getToolByName


def install(portal):
    """ This legacy install is needed because we need to uninstall genweb.theme
        *before* we run the steps from the alternatheme profile. All other
        options (importstep, uninstall profile) run after run the alternatheme
        profile.
    """
    tool = getToolByName(portal, 'portal_quickinstaller')
    setup_tool = getToolByName(portal, 'portal_setup')

    if tool.isProductInstalled('genweb.theme'):
        tool.uninstallProducts(['genweb.theme'])
    print " ====== Uninstalled genweb.theme from site"

    setup_tool.runAllImportStepsFromProfile('profile-genweb.alternatheme:default')


# def uninstall(portal):
#     setup_tool = getToolByName(portal, 'portal_setup')
#     setup_tool.runAllImportStepsFromProfile('profile-plonetheme.classic:uninstall')
#     return "Ran all uninstall steps."
