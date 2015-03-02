from plone.app.folder.folder import ATFolderSchema
from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import ImageField
from Products.Archetypes.atapi import ImageWidget
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextField
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from younglives.publication import _

YLPublicationSchema = ATFolderSchema.copy() + Schema((

    StringField(
        'subtitle',
        required=0,
        searchable=1,
        storage=AnnotationStorage(),
        widget=StringWidget(
            label=_(u"ylpublication_subtitle_label",
                    default=u"Subtitle"),
            description=_(u"ylpublication_subtitle_desc",
                          default=u"Enter publication subtitle."),),
    ),

    TextField(
        'text',
        required=False,
        searchable=True,
        primary=True,
        storage=AnnotationStorage(),
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=RichWidget(
            description='',
            label=_(u'label_body_text', default=u'Body Text'),
            rows=25,
            allow_file_upload=zconf.ATDocument.allow_document_upload),
    ),

    StringField(
        'author',
        required=1,
        searchable=1,
        storage=AnnotationStorage(),
        widget=StringWidget(
            label=_(u"ylpublication_author_label",
                    default=u"Author"),
            description=_(u"ylpublication_author_desc",
                          default=u"Enter publication's author."),),
    ),

    StringField(
        'series',
        required=0,
        searchable=1,
        storage=AnnotationStorage(),
        widget=StringWidget(
            label=_(u"ylpublication_series_label",
                    default=u"Series"),
            description=_(u"ylpublication_series_desc",
                          default=u"Enter publication's series."),),
        ),

    DateTimeField(
        'publication_date',
        required=1,
        searchable=0,
        languageIndependent=1,
        storage=AnnotationStorage(),
        widget=CalendarWidget(
            show_hm=False,
            label=_(u"ylpublication_publication_date_label",
                    default=u"Date"),
            description=_(u"ylpublication_publication_date_desc",
                          default=u"Publication date"),),
        ),

    ImageField(
        'cover_image',
        required=0,
        searchable=0,
        languageIndependent=1,
        sizes={
            'thumb': (80, 80),
            'preview': (150, 150),
        },
        widget=ImageWidget(
            label=_(u"ylpublication_cover_image_label",
                    default=u"Cover Image"),
            description=_(u"ylpublication_cover_image_desc",
                          default=u"Image size should be XXX"),),
        ),

))

finalizeATCTSchema(YLPublicationSchema, moveDiscussion=False)
