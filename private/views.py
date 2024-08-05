from typing import Any
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
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

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Input Laporan Berhasil!")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Input Laporan Gagal! Ada yang salah salam pengisian. Mohon dicek ulang atau hubungi Administrator.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class PrivateDetailView(LoginRequiredMixin, DetailView):
    model = Private

class PrivateUpdateView(LoginRequiredMixin, UpdateView):
    model = Private
    form_class = PrivateUpdateForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Update Laporan Berhasil!")
        self.object = form.save()
        return HttpResponseRedirect(reverse("private:private-update", kwargs={"pk": self.kwargs.get("pk")}))
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Laporan Gagal! Ada yang salah salam pengisian. Mohon dicek ulang atau hubungi Administrator.")
        return super().form_invalid(form)

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