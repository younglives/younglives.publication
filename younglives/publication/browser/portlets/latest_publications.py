from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter

from younglives.publication import _


class ILatestPublicationsPortlet(IPortletDataProvider):
    """ A portlet which shows latest publications. """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        required=1,
        default=u"New Publications")

    count = schema.Int(
        title=_(u'Number of items to display'),
        required=1,
        default=5)


class Assignment(base.Assignment):
    implements(ILatestPublicationsPortlet)

    header = u"New Publications"
    item_types = ()
    count = 5

    def __init__(self, header=u"New Publications", count=5):
        super(Assignment, self).__init__()
        self.header = header
        self.count = count

    @property
    def raw_title(self):
        return u"New Publications"

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('latest_publications.pt')

    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return True

    def items(self):
        return self._data()

    def title(self):
        return self.data.title

    @memoize
    def _data(self):
        limit = self.data.count
        # If limit set to 0,
        # return an empty list (displaying only image and text)
        if limit < 1:
            return []

        catalog = getMultiAdapter((self.context, self.request),
                                  name="plone_tools").catalog()

        latest = catalog(
            portal_type='YLPublication',
            sort_on='publication_date',
            sort_order='reverse',
            sort_limit=limit,
        )
        return latest


class AddForm(base.AddForm):
    """ Portlet add form. """

    form_fields = form.Fields(ILatestPublicationsPortlet)

    label = _(u"portlet_latest-items_add_title",
              default=u"Add latest items portlet")
    description = _(u"portlet_latest-items_add_desc",
                    default=u"A portlet which displays latest items")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """ Portlet edit form. """

    form_fields = form.Fields(ILatestPublicationsPortlet)
    label = _(u"portlet_latest-items_edit_title",
              default=u"Edit latest items portlet")
    description = _(u"portlet_latest-items_edit_desc",
                    default=u"A portlet which displays latest items")
