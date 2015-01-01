from Acquisition import aq_parent, aq_inner

from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite


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
    """
    Import various settings."""
    # Only run step if a flag file is present
    if context.readDataFile('younglives.publication.txt') is None:
        return
    catalog = getToolByName(getSite(), 'portal_catalog')
    items = catalog.searchResults({'meta_type': 'Publication', })
    for item in items[:1]:
        object = item.getObject()
        parent_folder = object.aq_inner.aq_parent
        parent_folder.invokeFactory(
            'YLPublication',
            object.getId() + '_new',
            title=object.Title(),
            description=object.description,
            text=object.getText())
        new_object = parent_folder[object.getId() + '_new']
        new_object.setAuthor(object.getAuthor())
        new_object.setSeries(object.getSeries())
        new_object.setPublication_date(object.getPublication_date())
        pub_files = object.getFiles()
        for pub_file in pub_files:
            move_object(ob=pub_file, dest=new_object)
        print len(pub_files)
    print 'finished'
