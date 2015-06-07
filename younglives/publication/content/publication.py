from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import registerType
from plone.app.folder.folder import ATFolder
from zope.interface import implements

from younglives.publication.config import PROJECTNAME
from younglives.publication.interfaces import IYLPublication

from schemata import YLPublicationSchema


class YLPublication(ATFolder):
    """A YoungLives publication"""
    implements(IYLPublication)
    security = ClassSecurityInfo()
    schema = YLPublicationSchema

    security.declarePublic('Title')
    def Title(self):
        title = self.Schema()['title'].get(self)
        if self.getSubtitle():
            return title + ': ' + self.getSubtitle()
        return title

    security.declarePublic('editTitle')
    def editTitle(self):
        return self.Schema()['title'].get(self)

registerType(YLPublication, PROJECTNAME)
