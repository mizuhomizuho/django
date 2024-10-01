from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import Views, LoginUserView, LoginViewFromDefAuthForm

app_name = 'app_users' # для include namespace

urlpatterns = [
    path('reg/', Views.reg, name='reg'),
    path('login/', Views.login, name='login'),
    path('login-view/', LoginUserView.as_view(), name='login_view'),
    path('login-def/', LoginViewFromDefAuthForm.as_view(), name='login_def'),
    # path('logout/', Views.logout, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
