from Products.Archetypes.atapi import registerType
from plone.app.folder.folder import ATFolder
from zope.interface import implements

from younglives.publication.config import PROJECTNAME
from younglives.publication.interfaces import IYLPublication

from schemata import YLPublicationSchema


class YLPublication(ATFolder):
    """A YoungLives publication"""
    implements(IYLPublication)

    schema = YLPublicationSchema

registerType(YLPublication, PROJECTNAME)
