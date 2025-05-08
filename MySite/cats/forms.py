from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from .models import Category, Owner, Cats
from django.core.validators import MinLengthValidator, MaxLengthValidator

@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'
    def __init__(self, message=None):
        self.message = message \
            if message \
            else "Должны присутствовать только русские символы, дефис и пробел."
    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                           empty_label="Категория не выбрана", label="Категории")
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(),
                           required=False, empty_label="Отсутствует", label="Владелец")

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

    class Meta:
        model = Cats
        fields = ['title', 'slug', 'content', 'photo', 'is_published',
                  'cat', 'owner', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class':
                                                'form-input'}),
            'slug': forms.TextInput(attrs={'class':
                                                'form-input'}),
            'content': forms.Textarea(attrs={'cols':
                                                 60, 'rows': 10}),
        }


#class UploadFileForm(forms.Form):
    #file = forms.FileField(label="Файл")

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")