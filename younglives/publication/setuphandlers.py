import logging
from zope.app.component.hooks import getSite

from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

def importVarious(context):
    """
    Import various settings."""
    # Only run step if a flag file is present
    if context.readDataFile('younglives.publication.txt') is None:
        return
    site = context.getSite()
    out = StringIO()
