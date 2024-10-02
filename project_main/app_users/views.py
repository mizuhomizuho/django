from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from . import forms
from .forms import PassChangeForm


class Views:

    @staticmethod
    def login(request):
        form = forms.CustomLoginUserForm()
        if request.POST.get('form_id') == 'form_login':
            form = forms.CustomLoginUserForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    request,
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user and user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('frontpage'))
        return render(request, 'app_users/custom_login_form.html', {
            'custom_form': form
        })

    @staticmethod
    def reg(request):
        form = forms.RegisterUserForm()
        if request.POST.get('form_id') == 'reg':
            form = forms.RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return render(request, 'app_users/reg_done.html')
        return render(request, 'app_users/reg.html', {
            'form': form
        })

    @staticmethod
    def logout(request):
        logout(request)
        return HttpResponseRedirect(reverse('users_namespace:login'))

class LoginUserView(LoginView):

    form_class = AuthenticationForm
    # template_name = 'app_users/login_view.html'
    extra_context = {
        'title': 'Авторизация (AuthenticationForm)'
    }

    # def get_success_url(self):
    #     return reverse_lazy('frontpage')

class LoginViewFromDefAuthForm(LoginView):

    form_class = forms.LoginUserForm
    extra_context = {
        'title': 'Авторизация (LoginUserForm from AuthenticationForm)'
    }

class RegUserFromUCF(CreateView):

    form_class = forms.RegisterFormFromUCF
    template_name = 'app_users/reg.html'
    extra_context = {
        'title': 'Register (RegUserFromUCF)'
    }
    success_url = reverse_lazy('users_namespace:login')

class ProfileUser(LoginRequiredMixin, UpdateView):

    model = get_user_model()
    form_class = forms.ProfileForm
    extra_context = {
        'title': 'Profile (ProfileUser)',
        'def_user_img': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users_namespace:profile')

    def get_object(self, queryset=None):
        return self.request.user

class PassChangeUser(LoginRequiredMixin, PasswordChangeView):
    form_class = PassChangeForm
    success_url = reverse_lazy('users_namespace:pass_change_done')
