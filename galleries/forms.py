from django import forms
from galleries.models import Gallery

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            "title" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "image" : forms.FileInput(attrs={"accept": ".jpg, .jpeg, .png", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 shadow-lg"}),
            "caption" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }
