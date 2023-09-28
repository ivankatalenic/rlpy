from django.urls import path

from . import views

urlpatterns = [
	path("check-braces/", views.check_braces, name="check-braces")
]
