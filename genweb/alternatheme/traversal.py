from plone.resource.traversal import ResourceTraverser


class GenwebTraverser(ResourceTraverser):
    """The Genweb alternatheme static resource traverser.

    Just to assure that the JS and CSS resources are well known and isolated
    Allows traversal to /++gw++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """

    name = 'gw'
