from typing import Any
from private.models import Private, Subject
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from private.forms import PrivateUpdateForm, SubjectUpdateForm

# Private Controllers
class PrivateIndexView(ListView):
    model = Private

class PrivateCreateView(LoginRequiredMixin, CreateView):
    model = Private
    form_class = PrivateUpdateForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class PrivateDetailView(LoginRequiredMixin, DetailView):
    model = Private

class PrivateUpdateView(LoginRequiredMixin, UpdateView):
    model = Private
    form_class = PrivateUpdateForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class PrivateDeleteView(LoginRequiredMixin, DeleteView):
    model = Private


# Subject Controllers
class SubjectIndexView(ListView):
    model = Subject

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectUpdateForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectUpdateForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject