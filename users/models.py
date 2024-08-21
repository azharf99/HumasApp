from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Username"),)
    niy = models.IntegerField(default=0, verbose_name=_("NIY"))
    nama_guru = models.CharField(max_length=100, verbose_name=_("Nama Guru"), default="Fulan")
    jenis_kelamin = models.CharField(max_length=1, choices=(("L", "Laki-Laki"), ("P", "Perempuan")), default="L", verbose_name=_("Jenis Kelamin"))
    alamat = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Alamat"))
    jabatan = models.CharField(max_length=100, blank=True, verbose_name=_("Jabatan"))
    email = models.EmailField(default='smaitalbinaa.ekskul@outlook.com', blank=True, verbose_name=_("Email"))
    no_hp = models.CharField(max_length=20, blank=True, default=0, verbose_name=_("Whatsapp"))
    foto = models.ImageField(upload_to='user', default='blank-profile.png', blank=True, null=True, help_text="format foto .jpg/.jpeg", verbose_name=_("Foto"))

    def __str__(self):
        return self.nama_guru

    def get_absolute_url(self):
        return reverse("profile")
    
    class Meta:
        ordering = ["nama_guru"]
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        db_table = "teachers"
        indexes = [
            models.Index(fields=["id","niy",]),
        ]
