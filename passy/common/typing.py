"""
Classes and items used for typing only
"""

from typing import Dict, Any

from django.core.handlers.wsgi import WSGIRequest

import django.contrib.auth.models


class Request(WSGIRequest):
    """
    Only used for typing, the WSGIRequest already contains all the properties defined here.
    """

    user: django.contrib.auth.models.User
    session: Dict[str, Any]
