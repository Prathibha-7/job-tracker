from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("applications/add/", views.application_create, name="application_create"),
    path(
        "applications/<int:pk>/edit/",
        views.application_update,
        name="application_update",
    ),
    path(
        "applications/<int:pk>/status/",
        views.application_update_status,
        name="application_update_status",
    ),
    path(
        "applications/<int:pk>/delete/",
        views.application_delete,
        name="application_delete",
    ),
]
