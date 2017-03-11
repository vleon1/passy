from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from passy.helpers import status


def redirect(name: str) -> HttpResponse:

    url = reverse(name)
    response = HttpResponseRedirect(url)
    response.status_code = status.HTTP_303_SEE_OTHER

    return response
