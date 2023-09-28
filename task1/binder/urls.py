from django.urls import path

from . import views

urlpatterns = [
	path("pair-names/", views.pair_names, name="pair-names"),
]
