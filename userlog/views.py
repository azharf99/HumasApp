from typing import Any
from django.forms import BaseModelForm
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from utils.mixins import GeneralAuthPermissionMixin, GeneralFormDeleteMixin, GeneralFormValidateMixin
from userlog.models import UserLog
from userlog.forms import UserlogCreateForm
from utils.whatsapp_albinaa import send_WA_create_update_delete


# Create your views here.

class UserLogListView(GeneralAuthPermissionMixin, ListView):
    model = UserLog
    paginate_by = 50

class UserLogCreateView(GeneralFormValidateMixin, CreateView):
    model = UserLog
    form_class = UserlogCreateForm
    app_name = "UserLog"
    form_name = "Create"
    type_url = 'userlog/'
    permission_required = 'userlog.add_userlog'


class UserLogDetailView(GeneralAuthPermissionMixin, DetailView):
    model = UserLog
    permission_required = 'userlog.add_userlog'

class UserLogUpdateView(GeneralFormValidateMixin, UpdateView):
    model = UserLog
    form_class = UserlogCreateForm
    app_name = "UserLog"
    form_name = "Update"
    type_url = 'userlog/'
    permission_required = 'userlog.change_userlog'
    
class UserLogDeleteView(GeneralFormDeleteMixin):
    model = UserLog
    success_url = reverse_lazy("userlog:userlog-index")
    app_name = "UserLog"
    type_url = 'userlog/'
    permission_required = 'userlog.delete_userlog'