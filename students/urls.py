from django.urls import path
from students.views import StudentIndexView, StudentCreateView, StudentDetailView, StudentUpdateView, StudentDeleteView, \
                            ClassIndexView, ClassCreateView, ClassDetailView, ClassUpdateView, ClassDeleteView
app_name = "student"

urlpatterns = [
    path("", StudentIndexView.as_view(), name="student-index"),
    path("create/", StudentCreateView.as_view(), name="student-create"),
    path("detail/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("update/<int:pk>/", StudentUpdateView.as_view(), name="student-update"),
    path("delete/<int:pk>/", StudentDeleteView.as_view(), name="student-delete"),
    path("class/", ClassIndexView.as_view(), name="class-index"),
    path("class/create/", ClassCreateView.as_view(), name="class-create"),
    path("class/detail/<int:pk>/", ClassDetailView.as_view(), name="class-detail"),
    path("class/update/<int:pk>/", ClassUpdateView.as_view(), name="class-update"),
    path("class/delete/<int:pk>/", ClassDeleteView.as_view(), name="class-delete"),
]