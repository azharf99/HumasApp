from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.urls import reverse_lazy
from alumni.models import Alumni
from alumni.forms import AlumniForm
from django.utils import timezone
from utils.whatsapp import send_whatsapp_humas
from userlog.models import UserLog


class AlumniDashboardView(ListView):
    model = Alumni
    template_name = 'alumni/alumni_dashboard.html'
    queryset = Alumni.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["jumlah_alumni_putra"] = self.queryset.filter(gender="L")
        c["jumlah_alumni_putri"] = self.queryset.filter(gender="P")
        c["jumlah_alumni_tahun_ini"] = self.queryset.filter(graduate_year=timezone.now().year)
        c["jumlah_alumni_putra_tahun_ini"] = self.queryset.filter(gender="L", graduate_year=timezone.now().year)
        c["jumlah_alumni_putri_tahun_ini"] = self.queryset.filter(gender="P", graduate_year=timezone.now().year)
        c["jumlah_alumni_universitas"] = self.queryset.filter(Q(undergraduate_university__isnull=False)|Q(postgraduate_university__isnull=False)|Q(doctoral_university__isnull=False))
        c["jumlah_alumni_putra_universitas"] = self.queryset.filter(Q(gender="L") & Q(undergraduate_university__isnull=False)|Q(postgraduate_university__isnull=False)|Q(doctoral_university__isnull=False))
        c["jumlah_alumni_putri_universitas"] = self.queryset.filter(Q(gender="P",) & Q(undergraduate_university__isnull=False)|Q(postgraduate_university__isnull=False)|Q(doctoral_university__isnull=False))
        c["logs"] = UserLog.objects.filter(app="Alumni").order_by("-created_at")
        c["sebaran_wilayah"] = Alumni.objects.values('city', 'province').annotate(dcount=Count('city'))
        c["sebaran_universitas_sarjana"] = self.queryset.values('undergraduate_university').annotate(dcount=Count('undergraduate_university')).order_by()
        c["sebaran_universitas_magister"] = self.queryset.values('postgraduate_university').annotate(dcount=Count('postgraduate_university')).order_by()
        c["sebaran_universitas_doktoral"] = self.queryset.values('doctoral_university').annotate(dcount=Count('doctoral_university')).order_by()
        return c


class AlumniIndexView(ListView):
    model = Alumni



class AlumniSearchView(ListView):
    model = Alumni
    template_name = 'alumni/alumni_search.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        query = request.GET.get("query")
        queryset = None
        if query:
            data = Alumni.objects.filter(Q(nis__icontains=query)|Q(name__icontains=query))
            if len(data) > 0:
                messages.success(request, f"{len(data)} Data Berhasil Ditemukan!")
            else:
                messages.error(request, "Data Tidak Ditemukan!")
            queryset = data
        self.object_list = queryset
        allow_empty = self.get_allow_empty()
        context = self.get_context_data()
        return self.render_to_response(context)


class AlumniCreateView(LoginRequiredMixin, CreateView):
    model = Alumni
    form_class = AlumniForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        send_whatsapp_humas(self.request.user.teacher.no_hp, "Input", f"{self.object.name}", f"angkatan {self.object.group}")
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "INPUT",
            app = "Alumni",
            message = f"{self.request.user.teacher} berhasil input data alumni atas nama {self.object.name} angkatan {self.object.group}"
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class AlumniQuickUploadView(LoginRequiredMixin, CreateView):
    model = Alumni
    form_class = AlumniForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        send_whatsapp_humas(self.request.user.teacher.no_hp, "Input", f"{self.object.name}", f"angkatan {self.object.group}")
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "INPUT",
            app = "Alumni",
            message = f"{self.request.user.teacher} berhasil input data alumni atas nama {self.object.name} angkatan {self.object.group}"
        )
        return super().form_valid(form)

class AlumniDetailView(LoginRequiredMixin, DetailView):
    model = Alumni

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AlumniUpdateView(LoginRequiredMixin, UpdateView):
    model = Alumni
    form_class = AlumniForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        send_whatsapp_humas(self.request.user.teacher.no_hp, "Edit", f"{self.object.name}", f"angkatan {self.object.group}")
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "EDIT",
            app = "Alumni",
            message = f"{self.request.user.teacher} berhasil edit data alumni atas nama {self.object.name} angkatan {self.object.group}"
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c


class AlumniDeleteView(LoginRequiredMixin, DeleteView):
    model = Alumni
    success_url = reverse_lazy("alumni:alumni-index")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        send_whatsapp_humas(self.request.user.teacher.no_hp, "Hapus", f"{self.object.name}", f"angkatan {self.object.group}")
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "HAPUS",
            app = "Alumni",
            message = f"{self.request.user.teacher} berhasil hapus data alumni atas nama {self.object.name} angkatan {self.object.group}"
        )
        return super().form_valid(form)