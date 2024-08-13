from django.urls import path
from tahfidz.views import TahfidzIndexView, TahfidzCreateView, TahfidzDetailView, TahfidzUpdateView, TahfidzDeleteView, \
                            TahfidzQuickUploadView, TahfidzQuickCSVUploadView
app_name = "tahfidz"

urlpatterns = [
    path("", TahfidzIndexView.as_view(), name="tahfidz-index"),
    path("create/", TahfidzCreateView.as_view(), name="tahfidz-create"),
    path("quick-create/", TahfidzQuickUploadView.as_view(), name="tahfidz-quick-create"),
    path("quick-create-csv/", TahfidzQuickCSVUploadView.as_view(), name="tahfidz-quick-create-csv"),
    path("detail/<int:pk>/", TahfidzDetailView.as_view(), name="tahfidz-detail"),
    path("update/<int:pk>/", TahfidzUpdateView.as_view(), name="tahfidz-update"),
    path("delete/<int:pk>/", TahfidzDeleteView.as_view(), name="tahfidz-delete"),
]