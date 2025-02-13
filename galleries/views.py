from django.shortcuts import render
from django.urls import reverse_lazy
from galleries.forms import GalleryForm
from galleries.models import Gallery
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

# Create your views here.
class GalleryListView(ListView):
    model = Gallery


class GalleryCreateView(CreateView):
    model = Gallery
    form_class = GalleryForm
    template_name = "alumni/files_form.html"

class GalleryUpdateView(UpdateView):
    model = Gallery
    form_class = GalleryForm
    template_name = "alumni/files_form.html"

class GalleryDetailView(DetailView):
    model = Gallery

class GalleryDeleteView(DeleteView):
    model = Gallery
    success_url = reverse_lazy("galleries:gallery-list")