from django import forms
from private.models import Subject, Private, Group
from students.models import Student
from users.models import Teacher

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            "pembimbing" : forms.SelectMultiple(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "nama_pelajaran" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['tahun_ajaran']
        widgets = {
            "nama_kelompok" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "jenis_kelompok" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "pelajaran" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "jadwal" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "waktu" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "santri" : forms.SelectMultiple(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }


class PrivateCreateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user', None)
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)

        subjects = subject.filter(pembimbing=user.teacher)
        group = Group.objects.select_related("pelajaran").prefetch_related("santri").filter(pelajaran__in=subjects)
        teacher_list = subjects.values_list("pembimbing", flat=True).distinct()
        
        if user.teacher.id in teacher_list:
            student_list = group.values_list("santri", flat=True).distinct()
            self.fields['pembimbing'].queryset = Teacher.objects.filter(pk__in=teacher_list)
            self.fields['kehadiran_santri'].queryset = Student.objects.filter(pk__in=student_list)
            self.fields['kelompok'].queryset = group
            self.fields['pelajaran'].queryset = subjects

    
    class Meta:
        model = Private
        fields = '__all__'
        exclude = ['tahun_ajaran']
        widgets = {
            "pembimbing" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "pelajaran" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "tanggal_bimbingan" : forms.DateInput(attrs={"type": "date", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "waktu_bimbingan" : forms.TimeInput(attrs={"type": "time", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "kelompok" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "kehadiran_santri" : forms.SelectMultiple(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "catatan_bimbingan" : forms.Textarea(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }


class PrivateUpdateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user', None)
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)

        subjects = subject.filter(pembimbing=user.teacher)
        group = Group.objects.select_related("pelajaran").prefetch_related("santri").filter(pelajaran__in=subjects)
        teacher_list = subjects.values_list("pembimbing", flat=True).distinct()
        
        if user.teacher.id in teacher_list:
            student_list = group.values_list("santri", flat=True).distinct()
            self.fields['pembimbing'].queryset = Teacher.objects.filter(pk__in=teacher_list)
            self.fields['kehadiran_santri'].queryset = Student.objects.filter(pk__in=student_list)
            self.fields['pelajaran'].queryset = subjects
    
    class Meta:
        model = Private
        fields = '__all__'
        exclude = ['tahun_ajaran']
        widgets = {
            "pembimbing" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "pelajaran" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "tanggal_bimbingan" : forms.DateInput(attrs={"type": "date", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "waktu_bimbingan" : forms.TimeInput(attrs={"type": "time", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "catatan_bimbingan" : forms.Textarea(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "kelompok" : forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "kehadiran_santri" : forms.SelectMultiple(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }