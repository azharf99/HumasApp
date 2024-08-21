from django.urls import path
from private.views import PrivateIndexView, PrivateCreateView, PrivateDetailView, PrivateUpdateView, PrivateDeleteView, \
                            SubjectIndexView, SubjectCreateView, SubjectDetailView, SubjectUpdateView, SubjectDeleteView, \
                            GroupIndexView, GroupCreateView, GroupDetailView, GroupUpdateView, GroupDeleteView,\
                            GroupGetView, GroupQuickUploadView, PrivatePrintView
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
    path("groups/", GroupIndexView.as_view(), name="group-index"),
    path("get-group/", GroupGetView.as_view(), name="group-get"),
    path("group/create/", GroupCreateView.as_view(), name="group-create"),
    path("group/quick-create/", GroupQuickUploadView.as_view(), name="group-quick-create"),
    path("group/detail/<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("group/update/<int:pk>/", GroupUpdateView.as_view(), name="group-update"),
    path("group/delete/<int:pk>/", GroupDeleteView.as_view(), name="group-delete"),
]