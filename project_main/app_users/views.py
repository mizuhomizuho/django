from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import LoginUserForm, CustomLoginUserForm, RegisterUserForm

class Views:

    @staticmethod
    def login(request):
        form = CustomLoginUserForm()
        if request.POST.get('form_id') == 'form_login':
            form = CustomLoginUserForm(request.POST)
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
        form = RegisterUserForm()
        if request.POST.get('form_id') == 'reg':
            form = RegisterUserForm(request.POST)
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

    form_class = LoginUserForm
    extra_context = {
        'title': 'Авторизация (LoginUserForm from AuthenticationForm)'
    }