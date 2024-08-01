from django import forms
from private.models import Subject, Private

class SubjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            "nama_pelajaran" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }


class PrivateUpdateForm(forms.ModelForm):
    class Meta:
        model = Private
        fields = '__all__'
        widgets = {
            "pembimbing" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "pelajaran" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "tanggal_bimbingan" : forms.DateInput(attrs={"type": "date", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "waktu_bimbingan" : forms.TimeInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "catatan_bimbingan" : forms.Textarea(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "kehadiran_santri" : forms.SelectMultiple(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }