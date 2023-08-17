from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path
from rest_framework.schemas import get_schema_view

from parking.urls import router

urlpatterns = [
    path('api_schema/', get_schema_view(
        title='API Schema',
        description='Guide for the REST API'
    ), name='schema_url'),
    path('docs', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'schema_url'}
    ), name='swagger-ui'),
    path("admin/", admin.site.urls),
    path("", include(router.urls))
]
