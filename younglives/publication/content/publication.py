from Products.Archetypes.atapi import registerType
from plone.app.folder.folder import ATFolder

from younglives.policy import _
from younglives.publication.config import PROJECTNAME

from schemata import YLPublicationSchema

class YLPublication(ATFolder):
    """A YoungLives publication"""

    schema = YLPublicationSchema

registerType(YLPublication, PROJECTNAME)
