from django.urls import path
from alumni.views import AlumniDashboardView, AlumniSearchView, AlumniIndexView, AlumniCreateView, \
                        AlumniDetailView, AlumniUpdateView, AlumniDeleteView, AlumniQuickUploadView

app_name = "alumni"

urlpatterns = [
    path("", AlumniIndexView.as_view(), name="alumni-index"),
    path("dashboard/", AlumniDashboardView.as_view(), name="alumni-dashboard"),
    path("search/", AlumniSearchView.as_view(), name="alumni-search"),
    path("create/", AlumniCreateView.as_view(), name="alumni-create"),
    path("quick-upload/", AlumniQuickUploadView.as_view(), name="alumni-quick-upload"),
    path("detail/<int:pk>/", AlumniDetailView.as_view(), name="alumni-detail"),
    path("update/<int:pk>/", AlumniUpdateView.as_view(), name="alumni-update"),
    path("delete/<int:pk>/", AlumniDeleteView.as_view(), name="alumni-delete"),
]