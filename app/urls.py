from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view

from parking.urls import router, parking_router, spot_router
from parking.views import DocumentationView

urlpatterns = [
    # TODO: This got broken by nested routers
    path(
        "api_schema/",
        get_schema_view(
            title="API Schema", description="This got broken by nested routers. I will fix it soon!"
        ),
        name="schema_url",
    ),
    path(
        "docs",
        DocumentationView.as_view(),
        name="swagger-ui",
    ),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include(parking_router.urls)),
    path("", include(spot_router.urls)),
]
