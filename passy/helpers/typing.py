"""
Classes and items used for typing only
"""

from typing import Dict, Any

from django.core.handlers.wsgi import WSGIRequest

from passy.models import User


class Request(WSGIRequest):
    """
    Only used for typing, the WSGIRequest already contains all the properties defined here.
    """

    user: User
    session: Dict[str, Any]
