from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username",)
    niy = models.IntegerField(default=0, verbose_name='NIY')
    nama_pembina = models.CharField(max_length=100, verbose_name="Nama Pembina")
    jenis_kelamin = models.CharField(max_length=1, choices=(("L", "Laki-Laki"), ("P", "perempuan")), default="L")
    alamat = models.CharField(max_length=100, blank=True, null=True)
    jabatan = models.CharField(max_length=100, blank=True)
    email = models.EmailField(default='smaitalbinaa.ekskul@outlook.com', blank=True)
    no_hp = models.CharField(max_length=20, blank=True, default=0)
    foto = models.ImageField(upload_to='user', default='blank-profile.png', blank=True, null=True, help_text="format foto .jpg/.jpeg")

    def __str__(self):
        return self.nama_pembina

    def get_absolute_url(self):
        return reverse("profil")
    
    class Meta:
        ordering = ["nama_pembina"]
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        db_table = "teachers"
        indexes = [
            models.Index(fields=["id","niy",]),
        ]
