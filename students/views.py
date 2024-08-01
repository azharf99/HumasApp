from typing import Any
from students.models import Student, Class
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Class Controllers
class ClassIndexView(ListView):
    model = Class

class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    fields = '__all__'

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class

class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = Class
    fields = '__all__'

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = Class


# Student Controllers
class StudentIndexView(ListView):
    model = Student

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student