from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base

from zope.i18nmessageid import MessageFactory
PLMF = MessageFactory('plonelocales')

from genweb.core import GenwebMessageFactory as TAM


class IEsdevenimentsPortlet(IPortletDataProvider):

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5,
                       min=5,
                       max=7)

    state = schema.Tuple(title=_(u"Workflow state"),
                         description=_(u"Items in which workflow state to show."),
                         default=('published', ),
                         required=True,
                         value_type=schema.Choice(
                             vocabulary="plone.app.vocabularies.WorkflowStates")
                         )


class Assignment(base.Assignment):
    implements(IEsdevenimentsPortlet)

    def __init__(self, count=5, state=('published', )):
        self.count = count
        self.state = state

    @property
    def title(self):
        return _(u"Events")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/esdeveniments.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()
        self.portal = portal_state.portal()
        self.navigation_root_path = portal_state.navigation_root_path()
        self.navigation_root_object = getNavigationRootObject(self.context, self.portal)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return self.data.count > 0 and len(self._data())

    def published_events(self):
        return self._data()

    def getMonthAbbr(self, data):
        context = aq_inner(self.context)
        month = DateTime.month(data)
        self._ts = getToolByName(context, 'translation_service')
        monthName = TAM(self._ts.month_msgid(month, format='a'),
                              default=self._ts.month_english(month, format='a'))
        return monthName

    def getMonth(self, data):
        context = aq_inner(self.context)
        month = DateTime.month(data)
        self._ts = getToolByName(context, 'translation_service')
        monthName = PLMF(self._ts.month_msgid(month),
                              default=self._ts.month_english(month))
        return monthName

    def getDay(self, data):
        day = str(DateTime.day(data))
        return day

    def sameDay(self, evento):
        if DateTime.Date(evento.start) == DateTime.Date(evento.end):
            return True
        else:
            return False

    @memoize
    def have_events_folder(self):
        return 'events' in self.navigation_root_object.objectIds()

    def all_events_link(self):
        if self.have_events_folder:
            events = self.portal.esdeveniments.getTranslation()
            return '%s' % events.absolute_url()
        else:
            return '%s/events_listing' % self.portal_url

    def prev_events_link(self):
        previous_events = self.portal.esdeveniments.aggregator.anteriors.getTranslation()
        if self.have_events_folder:
            return '%s' % previous_events.absolute_url()
        else:
            return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = self.data.count
        state = self.data.state
        now = DateTime()
        tomorrow = DateTime.Date(now + 1)
        yesterday = DateTime.Date(now - 1)
        path = self.navigation_root_path
        results = catalog(portal_type='Event',
                          review_state=state,
                          end={'query': now,
                               'range': 'min'
                               },
                          start={'query': [yesterday, tomorrow],
                               'range': 'min:max'
                               },
                          path=path,
                          sort_on='start',
                          sort_limit=limit)[:limit]
        count = len(results)
        if count < limit:
            results2 = catalog(portal_type=('Event'),
                       review_state=state,
                       end={'query': now,
                            'range': 'min'
                            },
                       start={'query': yesterday,
                              'range': 'max'
                            },
                       path=path,
                       sort_on='start',
                       sort_limit=limit - count)[:limit - count]
            count = len(results + results2)
            if count < limit:
                results3 = catalog(portal_type=('Event'),
                           review_state=state,
                           end={'query': now,
                                'range': 'min'
                                },
                       start={'query': tomorrow,
                              'range': 'min'
                            },
                       path=path,
                       sort_on='start',
                       sort_limit=limit - count)[:limit - count]
                return results + results2 + results3
            else:
                return results + results2
        else:
            return results


class AddForm(base.AddForm):
    form_fields = form.Fields(IEsdevenimentsPortlet)
    label = _(u"Add Events Portlet")
    description = _(u"This portlet lists upcoming Events.")

    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published', )))


class EditForm(base.EditForm):
    form_fields = form.Fields(IEsdevenimentsPortlet)
    label = _(u"Edit Events Portlet")
    description = _(u"This portlet lists upcoming Events.")
