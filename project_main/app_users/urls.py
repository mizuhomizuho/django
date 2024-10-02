from re import template

from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages import success
from django.urls import path, reverse_lazy
from .views import Views, LoginUserView, LoginViewFromDefAuthForm, RegUserFromUCF, ProfileUser, PassChangeUser

app_name = 'app_users' # для include namespace

urlpatterns = [
    path('reset-pass/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='app_users/reset_pass_confirm.html',
        success_url=reverse_lazy('users_namespace:reset_pass_done')
    ), name='reset_pass_confirm'),
    path('reset-pass/complete/', PasswordResetCompleteView.as_view(template_name='app_users/reset_pass_complete.html'), name='reset_pass_complete'),
    path('reset-pass/', PasswordResetView.as_view(
        template_name='app_users/reset_pass.html',
        email_template_name='app_users/reset_pass_email.html',
        success_url=reverse_lazy('users_namespace:reset_pass_done')
    ), name='reset_pass'),
    path('reset-pass/done/', PasswordResetDoneView.as_view(template_name='app_users/reset_pass_done.html'), name='reset_pass_done'),
    # path('pass_change/', PasswordChangeView.as_view(), name='pass_change'),
    path('pass_change/', PassChangeUser.as_view(), name='pass_change'),
    path('pass_change/done/', PasswordChangeDoneView.as_view(template_name='app_users/pass_change_done.html'), name='pass_change_done'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('reg/', Views.reg, name='reg'),
    path('reg-from-ucf/', RegUserFromUCF.as_view(), name='reg_from_ucf'),
    path('login/', Views.login, name='login'),
    path('login-view/', LoginUserView.as_view(), name='login_view'),
    path('login-def/', LoginViewFromDefAuthForm.as_view(), name='login_def'),
    path('logout/', Views.logout, name='logout'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]
