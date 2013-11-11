from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import ImageField
from Products.Archetypes.atapi import ImageWidget
from Products.Archetypes.atapi import ReferenceField
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import TextField
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interfaces.topic import IATTopic

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.OrderableReferenceField import OrderableReferenceField, OrderableReferenceWidget

from younglives.homepage import _

YLPublicationSchema = ATContentTypeSchema.copy() + Schema((

    StringField('subtitle',
        required = 0,
        searchable = 1,
        storage = AnnotationStorage(),
        widget = StringWidget(
            label = _(u"ylpublication_subtitle_label",
                      default = u"Subtitle"),
            description = _(u"ylpublication_subtitle_desc",
                            default = u"Enter publication subtitle."),)),

    StringField('author',
        required = 1,
        searchable = 1,
        storage = AnnotationStorage(),
        widget = StringWidget(
            label = _(u"ylpublication_author_label",
                      default = u"Author"),
            description = _(u"ylpublication_author_desc",
                            default = u"Enter publication's author."),)),

    StringField('series',
        required = 0,
        searchable = 1,
        storage = AnnotationStorage(),
        widget = StringWidget(
            label = _(u"ylpublication_series_label",
                      default = u"Series"),
            description = _(u"ylpublication_series_desc",
                            default = u"Enter publication's series."),)),

    DateTimeField('publication_date',
        required = 1,
        searchable = 0,
        languageIndependent = 1,
        storage = AnnotationStorage(),
        widget = CalendarWidget(
            label = _(u"ylpublication_publication-date_label",
                      default = u"Date"),
            description = _(u"ylpublication_publication-date_desc",
                            default = u"Publication date"),)),

))

finalizeATCTSchema(YLPublicationSchema, moveDiscussion=False)
