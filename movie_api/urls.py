from django.http import HttpResponse
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", lambda _: HttpResponse("OK"), name="root")
]

