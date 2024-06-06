from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path("", lambda _: HttpResponse("App running correctly!"), name="root"),
    path("draw-chart/", views.graph_endpoint, name="draw_chart"),
    path("load-data/", views.load_data_endpoint, name="load_data"),
    path("export-data/", views.export_data, name="export_data"),
]
