from django import forms
from users.models import Teacher

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            "user" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "niy" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "nama_pembina" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "jenis_kelamin" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "alamat" : forms.Textarea(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "jabatan" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "email" : forms.EmailInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "no_hp" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }