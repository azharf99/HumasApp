from io import BytesIO
from typing import Any
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.generic import DeleteView, View, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from utils.whatsapp_albinaa import send_WA_create_update_delete, send_WA_general
from userlog.models import UserLog
from xlsxwriter import Workbook


class GeneralContextMixin(View):
    form_name = ''

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = self.form_name
        c["query"] = self.request.GET.get("query")
        c["month"] = self.request.GET.get("month")
        c["year"] = self.request.GET.get("year")
        return c


class GeneralAuthPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin, GeneralContextMixin):
    raise_exception = True


class GeneralFormValidateMixin(GeneralAuthPermissionMixin, FormView):
    success_message: str = "Input data berhasil!"
    error_message: str = "Gagal input data. Ada sesuatu yang salah!"
    app_name = ''
    type_url = ''
    slug_url = ''

    def form_valid(self, form: Any) -> HttpResponse:
        self.object = form.save()
        messages.success(self.request, self.success_message)
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = self.form_name.upper(),
            app = self.app_name.upper(),
            message = f"berhasil {self.form_name.lower()} data {self.app_name} dengan detail berikut: {self.object}"
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, self.form_name.lower(), f'data {self.app_name} dengan detail berikut: {self.object}', self.type_url, self.slug_url)
        return super().form_valid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        messages.success(self.request, self.error_message)
        return super().form_invalid(form)
    

class GeneralFormDeleteMixin(GeneralAuthPermissionMixin, DeleteView):
    app_name = ''
    type_url = ''
    slug_url = ''

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = 'DELETE',
            app = self.app_name.upper(),
            message = f"berhasil menghapus data {self.app_name} dengan detail berikut: {self.obj}"
        )
        send_WA_create_update_delete(request.user.teacher.no_hp, 'menghapus', f'data {self.app_name} dengan detail berikut: {self.obj}', self.type_url, self.slug_url)
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)
    


class GeneralDownloadExcelView(GeneralAuthPermissionMixin):
    header_names = []
    filename = ''
    queryset = None
    app_name = ''

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        query = self.request.GET.get("query")
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, self.header_names)
        row = 1
        for data in self.queryset.filter(Q(nis__icontains=query)|
                                         Q(name__icontains=query)|
                                         Q(nisn__icontains=query)|
                                         Q(group__icontains=query)|
                                         Q(graduate_year__icontains=query)|
                                         Q(undergraduate_university__icontains=query)|
                                         Q(undergraduate_university_entrance__icontains=query)|
                                         Q(undergraduate_department__icontains=query)):
            if self.app_name == 'Alumni':
                worksheet.write_row(row, 0, [row, f"{data.nis}", f"{data.nisn}", data.name, data.group, data.graduate_year])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)


        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DOWNLOAD",
            app=self.app_name.upper(),
            message=f"berhasil download daftar {self.app_name.lower()} dalam format Excel"
        )
        send_WA_general(request.user.teacher.no_hp, 'download', f'file Excel data {self.app_name.lower()}')
        return FileResponse(buffer, as_attachment=True, filename=self.filename)