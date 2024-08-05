from django.urls import path
from users.views import TeacherCreateView, TeacherUpdateView, TeacherDeleteView, TeacherListView, TeacherDetailView

urlpatterns = [
    path('', TeacherListView.as_view(), name='teacher-list'),
    path('create/', TeacherCreateView.as_view(), name='teacher-create'),
    path('<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('update/<int:pk>/', TeacherUpdateView.as_view(), name='teacher-update'),
    path('delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher-delete'),
]