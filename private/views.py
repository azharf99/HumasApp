from typing import Any
from django.conf import settings
from django.contrib import messages
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from pandas import read_excel
from alumni.forms import FilesForm
from alumni.models import Files
from private.models import Private, Subject, Group
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from private.forms import PrivateCreateForm, PrivateUpdateForm, SubjectForm, GroupForm
from students.models import Student
from userlog.models import UserLog
from utils.whatsapp import send_WA_create_update_delete
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.utils import timezone


# Private Controllers
class PrivateIndexView(ListView):
    model = Private

class PrivateCreateView(LoginRequiredMixin, CreateView):
    model = Private
    form_class = PrivateCreateForm

    def get_form_kwargs(self) -> dict[str, Any]:
        k = super().get_form_kwargs()
        k["user"] = self.request.user
        k["subject"] = Subject.objects.prefetch_related("pembimbing").all()
        return k
    

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CREATE",
            app="PRIVATE",
            message=f"berhasil menambahkan data privat {self.object}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data privat {self.object}', 'private/')
        messages.success(self.request, "Input Laporan Berhasil!")
        return HttpResponseRedirect(self.get_success_url())
    
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

    def get_form_kwargs(self) -> dict[str, Any]:
        k = super().get_form_kwargs()
        k["user"] = self.request.user
        k["subject"] = Subject.objects.prefetch_related("pembimbing").all()
        return k

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.get_object().pembimbing == request.user.teacher or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="UPDATE",
            app="PRIVATE",
            message=f"berhasil mengubah data privat {self.object}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'mengubah', f'data privat {self.object}', 'private/')
        messages.success(self.request, "Update Laporan Berhasil!")
        return HttpResponseRedirect(reverse("private:private-detail", kwargs={"pk": self.kwargs.get("pk")}))
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Laporan Gagal! Ada yang salah salam pengisian. Mohon dicek ulang atau hubungi Administrator.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class PrivateDeleteView(LoginRequiredMixin, DeleteView):
    model = Private
    success_url = reverse_lazy("private:private-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.get_object().pembimbing == request.user.teacher or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="PRIVATE",
            message=f"berhasil menghapus data privat {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data privat {self.obj}', 'private/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)


# Subject Controllers
class SubjectIndexView(ListView):
    model = Subject

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CREATE",
            app="SUBJECT",
            message=f"berhasil menambahkan data mapel {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data mapel {self.obj}', 'private/', 'subjects/')
        messages.success(self.request, "Input Mapel Berhasil!")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Input Mapel Gagal!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="UPDATE",
            app="SUBJECT",
            message=f"berhasil update data mapel {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'update', f'data mapel {self.obj}', 'private/', 'subjects/')
        messages.success(self.request, "Update Mapel Berhasil!")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Mapel Gagal!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("private:subject-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="SUBJECT",
            message=f"berhasil menghapus data mapel {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data mapel {self.obj}', 'private/', 'subjects/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)
    


# Group Controllers
class GroupIndexView(ListView):
    model = Group

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CREATE",
            app="GROUP",
            message=f"berhasil menambahkan data kelompok privat {self.object}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data kelompok privat {self.object}', 'private/')
        messages.success(self.request, "Input Laporan Berhasil!")
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Input Laporan Gagal! Ada yang salah salam pengisian. Mohon dicek ulang atau hubungi Administrator.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c


class GroupQuickUploadView(LoginRequiredMixin, CreateView):
    model = Files
    form_class = FilesForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        df = read_excel(self.object.file, na_filter=False, dtype={"NIS": str})
        row, _ = df.shape
        try:
            for i in range(row):
                obj, created = Group.objects.update_or_create(
                    nama_kelompok = df.iloc[i, 0],
                    jenis_kelompok = df.iloc[i, 1],
                    pelajaran = Subject.objects.get(pk=df.iloc[i, 2]),
                    defaults=dict(
                        jadwal = df.iloc[i, 3],
                        waktu = df.iloc[i, 4]
                    )
                )
                obj.santri.add(Student.objects.get(nis=df.iloc[i, 5]))
                obj.save()
        except:
            messages.error(self.request, "Data pada Excel TIDAK SESUAI FORMAT! Mohon sesuaikan dengan format yang ada. Hubungi Administrator jika kesulitan.")
            return HttpResponseRedirect(reverse("private:group-index"))
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "CREATE",
            app = "GROUP",
            message = f"berhasil impor data excel kelompok privat"
        )
        messages.success(self.request, "Selamat, Impor data excel kelompok privat berhasil!")
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'mengimpor dari excel', 'data kelompok privat', 'private/', 'groups/')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import Excel Kelompok Privat"
        return c



class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="UPDATE",
            app="GROUP",
            message=f"berhasil mengubah data kelompok privat {self.object}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'mengubah', f'data kelompok privat {self.object}', 'private/')
        messages.success(self.request, "Update Laporan Berhasil!")
        return HttpResponseRedirect(reverse("private:group-detail", kwargs={"pk": self.kwargs.get("pk")}))
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Laporan Gagal! Ada yang salah salam pengisian. Mohon dicek ulang atau hubungi Administrator.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy("private:group-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="GROUP",
            message=f"berhasil menghapus data kelompok privat {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data kelompok privat {self.obj}', 'private/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)


class GroupGetView(LoginRequiredMixin, DetailView):
    model = Group

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        query = request.GET.get("query")
        if query:
            data = list(Group.objects.filter(pk=query).values("santri", "santri__nama_siswa", "santri__kelas__nama_kelas"))
            extra_data = list(Student.objects.select_related("kelas").filter(kelas__nama_kelas__startswith="XII").exclude(pk__in=Group.objects.filter(pk=query).values_list("santri")).values("id", "nama_siswa", "kelas__nama_kelas"))
            full_data = dict()
            full_data["utama"] = data
            full_data["ekstra"] = extra_data
            return JsonResponse(full_data, safe=False)
        else:
            data = {
                "utama": [
                    {
                    "santri": None,
                    "santri__nama_siswa": "Error! Harus Pilih Kelompok!"
                    },
                    {
                    "santri": None,
                    "santri__nama_siswa": "Jika Bingung, Hubungi Admin!"
                    }
                ]
            }

        return JsonResponse(data, safe=False)


class PrivatePrintView(LoginRequiredMixin, ListView):
    model = Private
    template_name = 'private/private_print.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        return Private.objects.filter(tanggal_bimbingan__month=timezone.now().month, tanggal_bimbingan__year=timezone.now().year).values("pembimbing__nama_guru").annotate(dcount=Count("pelajaran"))
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        MONTHS = {
            1: "Januari",
            2: "Februari",
            3: "Maret",
            4: "April",
            5: "Mei",
            6: "Juni",
            7: "Juli",
            8: "Agustus",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Desember",
        }
        c["tahun_ajaran"] = settings.TAHUN_AJARAN
        c["bulan_privat"] = MONTHS.get(timezone.now().month)
        c["site_title"] = f"Rekap Privat {c['bulan_privat']} {timezone.now().year}"
        c["jumlah_privat"] = Private.objects.filter(tanggal_bimbingan__month=timezone.now().month, tanggal_bimbingan__year=timezone.now().year).all()
        return c
    