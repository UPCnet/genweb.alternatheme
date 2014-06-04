from plone.resource.traversal import ResourceTraverser


class ComponentsTraverser(ResourceTraverser):
    """The bootstrap resources traverser.

    Allows traversal to /++components++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """

    name = 'components'


class GenwebTraverser(ResourceTraverser):
    """The Genweb theme traverser.

    Allows traversal to /++gw++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """

    name = 'gw'
