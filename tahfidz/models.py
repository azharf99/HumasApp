from django.db import models
from django.utils.translation import gettext as _
from students.models import Student
from django.urls import reverse

# Create your models here.
class Tahfidz(models.Model):
    santri = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_("Santri"))
    hafalan = models.CharField(_("Juz yang dihafal"), max_length=255)
    pencapaian_sebelumnya = models.CharField(_("Pencapaian Sebelumnya"), max_length=255, blank=True, null=True)
    pencapaian_sekarang = models.CharField(_("Pencapaian Sekarang"), max_length=255, blank=True, null=True)
    catatan = models.CharField(_("Catatan"), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.santri} - {self.hafalan}"
    

    def get_absolute_url(self):
        return reverse("tahfidz:tahfidz-create")
    
    class Meta:
        ordering = ["-santri"]
        verbose_name = _("Tahfidz")
        verbose_name_plural = _("Tahfidz")
        db_table = "tahfidz"
        indexes = [
            models.Index(fields=["id",]),
        ]