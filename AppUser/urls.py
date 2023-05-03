from django.urls import path

from .views import LoginView, GetAccessTokenView


urlpatterns = [
    path('login-step1/', LoginView.as_view({'post': 'login_step_1'}), name='login_step_1_view'),
    path('login-step2/', LoginView.as_view({'post': 'login_step_2'}), name='login_step_2_view'),
    path('get-access-token/', GetAccessTokenView.as_view(), name='access_token_view'),
]