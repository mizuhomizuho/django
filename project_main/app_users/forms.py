import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

class CustomLoginUserForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput)

class LoginUserForm(AuthenticationForm):
    pass
    # username = forms.CharField(label='Логин')
    # password = forms.CharField(widget=forms.PasswordInput)
    #
    # class Meta:
    #     model = get_user_model()
    #     fields = ('username', 'password')

class RegisterFormFromUCF(UserCreationForm):

    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
        labels = {
            'password2': 'Повторите пароль',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой Email уже существует')
        return self.cleaned_data.get('email')

class RegisterUserForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = get_user_model()
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
        labels = {
            'password2': 'Повторите пароль',
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password or password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data.get('password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой Email уже существует')
        return self.cleaned_data.get('email')

class ProfileForm(forms.ModelForm):

    username = forms.CharField(disabled=True)
    email = forms.EmailField(disabled=True)
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))

    class Meta:

        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'date_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'border: 1px solid red;'}),
        }

class PassChangeForm(PasswordChangeForm):

    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)