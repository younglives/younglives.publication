from Products.Archetypes.atapi import registerType
from Products.ATContentTypes.content.document import ATDocument

from younglives.policy import _
from younglives.publication.config import PROJECTNAME

class YLPublication(ATDocument):
    """A YoungLives publication"""

registerType(YLPublication, PROJECTNAME)
