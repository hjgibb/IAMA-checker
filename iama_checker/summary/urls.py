from django.urls import path

from . import views

app_name = "summary"

urlpatterns = [
    path("create_summary/<int:assessment_id>/", views.create_summary, name="create_summary"),
]
