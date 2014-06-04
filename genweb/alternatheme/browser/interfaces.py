from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IGenwebTheme(IDefaultPloneLayer):
    """Marker interface that defines a Zope browser layer."""


class IHomePageView(Interface):
    """Marker interface for the Homepage View."""
