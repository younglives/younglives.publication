from Acquisition import aq_inner
from Acquisition import aq_parent
from HTMLParser import HTMLParser
from plone.app.linkintegrity.exceptions \
    import LinkIntegrityNotificationException
from plone.app.linkintegrity.info import LinkIntegrityInfo
from Products.Archetypes.event import ObjectEditedEvent
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
import transaction
from zope.app.component.hooks import getSite
from zope.lifecycleevent import modified
from zope.publisher.interfaces import NotFound
import zope.event

referencedRelationship = 'isReferencing'

images_to_keep = [
    'changing-lives-in-a-changing-world-pub',
    'NothingisImpossible_coverscan.jpg',
    'pp6-murray',
]


class my_parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.images = []

    def handle_starttag(self, tag, attr):
        if tag == 'img':
            for item in attr:
                if item[0] == 'src':
                    self.images.append(item[1])


class TagDropper(HTMLParser):
    def __init__(self, tags_to_drop, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._text = []
        self._tags_to_drop = set(tags_to_drop)
    def clear_text(self):
        self._text = []
    def get_text(self):
        return ''.join(self._text)
    def handle_starttag(self, tag, attrs):
        if tag not in self._tags_to_drop:
            self._text.append(self.get_starttag_text())
    def handle_endtag(self, tag):
        if tag not in self._tags_to_drop:
            self._text.append('</{0}>'.format(tag))
    def handle_data(self, data):
        self._text.append(data)


def move_object(id_=None, ob=None, parent=None, dest=None, newid=None):
    # Either provide id and parent, or ob.
    if id_ is None:
        id_ = ob.getId()
    if parent is None:
        parent = aq_parent(aq_inner(ob))
    clipboard = parent.manage_cutObjects([id_])
    result = dest.manage_pasteObjects(clipboard)
    if newid is not None:
        dest.manage_renameObject(result['new_id'], newid)


def importVarious(context):
    """Migrate publications.
    """
    portal = getSite()
    catalog = getToolByName(portal, 'portal_catalog')
    refcat = getToolByName(portal, 'reference_catalog')
    wftool = getToolByName(portal, 'portal_workflow')
    items = catalog.searchResults({'meta_type': 'Publication', })
    parser = my_parser()
    tag_dropper = TagDropper(['img',])
    failed_covers = []
    broken_references = []
    for item in items:
        transaction.begin()
        object = item.getObject()
        object_id = object.getId()
        if object_id != 'nutritional-trajectories-in-childhood-Peru-Spanish':
            pass
        body_text = object.getText()
        parent_folder = object.aq_inner.aq_parent
        parent_folder.manage_renameObject(object_id, object_id + "-old")
        parent_folder.invokeFactory(
            'YLPublication',
            object_id,
            title=object.Title(),
            description=object.description)
        new_object = parent_folder[object_id]
        zope.event.notify(ObjectInitializedEvent(new_object))
        new_object.setAuthor(object.getAuthor())
        new_object.setSeries(object.getSeries())
        new_object.setPublication_date(object.getPublication_date())
        pub_files = object.getFiles()
        for pub_file in pub_files:
            move_object(ob=pub_file, dest=new_object)
        # delete the file references
        object.setFiles([])
        parser.images = []
        parser.feed(body_text)
        if len(parser.images) == 1:
            # only one image, so assume it's the cover
            #if len(parser.images[0]) > 28:
            if parser.images[0].find('publication-cover-images') > -1:
                path = parser.images[0].split('/')
                if path[3] in ['portal', 'ethiopia', 'india', 'vietnam',]:
                    path = '/'.join(path[4:])
                else:
                    path = '/'.join(path[3:])
                path = path.split('@@images')
                path = path[0]
                try:
                    the_image = portal.unrestrictedTraverse(path)
                except (NotFound, AttributeError):
                    pass
                else:
                    new_object.setCover_image(the_image.data)
                tag_dropper.feed(body_text)
                new_body_text = tag_dropper.get_text()
                new_object.setText(new_body_text)
                zope.event.notify(ObjectEditedEvent(new_object))
                modified(new_object)
                # remove the reference to the image
                object.setText(new_body_text)
                object.reindexObject()
                zope.event.notify(ObjectEditedEvent(object))
                modified(object)
                # delete the image
                image_folder = the_image.aq_inner.aq_parent
                if the_image.getId() not in images_to_keep:
                    try:
                        image_folder.manage_delObjects([the_image.getId(),])
                    except LinkIntegrityNotificationException:
                        pass
            else:
                failed_covers.append(object.getId())
                new_object.setText(body_text)
        else:
            failed_covers.append(object.getId())
            new_object.setText(body_text)
        new_object.reindexObject()
        try:
            parent_folder.manage_delObjects([object.getId(),])
        except LinkIntegrityNotificationException:
            broken_references.append(object.id)
        publish_new = True
        try:
            wftool.doActionFor(object, 'retract')
        except WorkflowException:
            # item not published
            publish_new = False
        if publish_new:
            try:
                wftool.doActionFor(new_object, 'publish')
            except WorkflowException:
                pass
        transaction.commit()
    return failed_covers, broken_references
