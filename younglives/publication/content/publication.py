from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import registerType
# need to import something from ATContentTypes
# otherwise an import error for folder occurs for tests
# http://stackoverflow.com/questions/21824850/test-module-import-failures-after-migrating-to-plone-app-testing-apparently-ci
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
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

    def publication_date(self):
        pub_date = self.getPublication_date()
        return pub_date

registerType(YLPublication, PROJECTNAME)
