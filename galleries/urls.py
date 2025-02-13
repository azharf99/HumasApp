from django.urls import path
from galleries.views import GalleryListView, GalleryCreateView, GalleryDetailView, GalleryUpdateView, GalleryDeleteView

app_name = "galleries"

urlpatterns = [
    path("", GalleryListView.as_view(), name="gallery-list"),
    path("create/", GalleryCreateView.as_view(), name="gallery-create"),
    path("detail/<int:pk>/", GalleryDetailView.as_view(), name="gallery-detail"),
    path("update/<int:pk>/", GalleryUpdateView.as_view(), name="gallery-update"),
    path("delete/<int:pk>/", GalleryDeleteView.as_view(), name="gallery-delete"),
]