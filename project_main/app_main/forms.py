from django import forms
from django.core.validators import MinLengthValidator
from django.utils.deconstruct import deconstructible
from app_catalog.models import Sections, Elements

@deconstructible
class NumValidator:

    __allow = '0123456789'
    __code = 'num_validator'

    def __init__(self, message=None):
        self.__message = message if message else 'Error Num Validator'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.__allow)):
            raise forms.ValidationError(self.__message, self.__code)

class SimpleForm(forms.Form):

    name = forms.CharField(
        error_messages={
            'required': 'Это поле обязательное',
        },
        label='Название'
    )
    code = forms.SlugField(max_length=255, validators=(
        MinLengthValidator(2),
        # NumValidator(),
    ))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 88}),
        required=False,
        max_length=88,
        min_length=8,
        error_messages={
            'min_length': 'Надо более длинный заголовок',
        },
    )
    is_active = forms.BooleanField(initial=True, required=False)
    parent = forms.ModelChoiceField(queryset=Sections.objects.all(), required=False, empty_label='Выбрать категорию...')
    files_img = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.jpeg,.jpg,.png', 'multiple': True})
    )

class AddElementForm(forms.ModelForm):

    class Meta:
        model = Elements
        # fields = '__all__'
        fields = ('name', 'code', 'description', 'is_active', 'photo')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'code': 'Slug'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('Error len(name) < 3', 'code_len_error')
        return name