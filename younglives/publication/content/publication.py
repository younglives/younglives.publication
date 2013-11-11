from Products.Archetypes.atapi import registerType
from Products.ATContentTypes.content.document import ATDocument

from younglives.policy import _
from younglives.publication.config import PROJECTNAME

from schemata import YLPublicationSchema

class YLPublication(ATDocument):
    """A YoungLives publication"""

    schema = YLPublicationSchema

registerType(YLPublication, PROJECTNAME)
