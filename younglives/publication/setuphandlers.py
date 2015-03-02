from Acquisition import aq_inner
from Acquisition import aq_parent
from HTMLParser import HTMLParser
from plone.app.linkintegrity.exceptions \
    import LinkIntegrityNotificationException
from plone.app.linkintegrity.info import LinkIntegrityInfo
from Products.Archetypes.event import ObjectEditedEvent
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
import transaction
from zope.app.component.hooks import getSite
from zope.lifecycleevent import modified
from zope.publisher.interfaces import NotFound
import zope.event

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
    items = catalog.searchResults({'meta_type': 'Publication', })
    parser = my_parser()
    tag_dropper = TagDropper(['img',])
    failed_covers = []
    for item in items:
        transaction.begin()
        object = item.getObject()
        object_id = object.getId()
        body_text = object.getText()
        parent_folder = object.aq_inner.aq_parent
        parent_folder.manage_renameObject(object_id, object_id + "-old")
        transaction.commit()
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
        parser.feed(body_text)
        if len(parser.images) == 1:
            # only one image, so assume it's the cover
            if len(parser.images[0]) > 28:
                path = parser.images[0].split('/')
                print path
                if path[3] in ['portal', 'ethiopia', 'india', 'vietnam',]:
                    path = '/'.join(path[4:])
                else:
                    path = '/'.join(path[3:])
                print path
                path = path.split('@@images')
                if len(path) > 1:
                    import pdb;pdb.set_trace()
                print path
                path = path[0]
                print path
                try:
                    the_image = portal.unrestrictedTraverse(path)
                except NotFound:
                    import pdb;pdb.set_trace()
                else:
                    new_object.setCover_image(the_image.data)
                # remove the image anyway, as it's broken
                tag_dropper.feed(body_text)
                new_body_text = tag_dropper.get_text()
                new_object.setText(new_body_text)
                new_object.reindexObject()
                zope.event.notify(ObjectEditedEvent(new_object))
                modified(new_object)
                # remove the reference to the image
                object.setText(new_body_text)
                object.reindexObject()
                zope.event.notify(ObjectEditedEvent(object))
                modified(object)
                # delete the image
                image_folder = the_image.aq_inner.aq_parent
                transaction.commit()
                transaction.begin()
                try:
                    image_folder.manage_delObjects([the_image.getId(),])
                    print 'Image deleted: ' + the_image
                except LinkIntegrityNotificationException:
                    # still linked by something else
                    import pdb;pdb.set_trace()
                    pass
            else:
                failed_covers.append(object.getId())
        else:
            failed_covers.append(object.getId())
        if object.getRelatedItems():
            print 'foobar'
            import pdb;pdb.set_trace()
        if object.getReferences():
            print 'foobar2'
            import pdb;pdb.set_trace()
        if object.getBackReferences():
            print 'foobar3'
            import pdb;pdb.set_trace()
        try:
            import pdb;pdb.set_trace()
            parent_folder.manage_delObjects([object.getId(),])
        except LinkIntegrityNotificationException:
            print 'barfoo'
            import pdb;pdb.set_trace()
        transaction.commit()
    return failed_covers
