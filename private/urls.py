from django.urls import path
from private.views import PrivateIndexView, PrivateCreateView, PrivateDetailView, PrivateUpdateView, PrivateDeleteView, \
                            SubjectIndexView, SubjectCreateView, SubjectDetailView, SubjectUpdateView, SubjectDeleteView, \
                            PrivatePrintView
app_name = "private"

urlpatterns = [
    path("", PrivateIndexView.as_view(), name="private-index"),
    path("create/", PrivateCreateView.as_view(), name="private-create"),
    path("detail/<int:pk>/", PrivateDetailView.as_view(), name="private-detail"),
    path("update/<int:pk>/", PrivateUpdateView.as_view(), name="private-update"),
    path("delete/<int:pk>/", PrivateDeleteView.as_view(), name="private-delete"),
    path("print/", PrivatePrintView.as_view(), name="private-print"),
    path("subjects/", SubjectIndexView.as_view(), name="subject-index"),
    path("subject/create/", SubjectCreateView.as_view(), name="subject-create"),
    path("subject/detail/<int:pk>/", SubjectDetailView.as_view(), name="subject-detail"),
    path("subject/update/<int:pk>/", SubjectUpdateView.as_view(), name="subject-update"),
    path("subject/delete/<int:pk>/", SubjectDeleteView.as_view(), name="subject-delete"),
]