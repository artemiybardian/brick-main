from django.urls import path
from authen.auth.views import (
    RegisterView, VerifyEmailView, LoginView,
    VerifyCodeView, CountryView, CityView
)
from authen.profile.views import ProfileAPIView
from authen.password_change.views import ChangePassword, RequestPasswordRestEmail, SetNewPasswordView


urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view()),
    path('verify/email/<uidb64>/<token>/', VerifyEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/code/email/', VerifyCodeView.as_view()),
    path('country/', CountryView.as_view()),
    path('city/<int:country_id>/', CityView.as_view()),
    # Profile
    path('profile', ProfileAPIView.as_view()),
    # Password
    path('profile/password/change/', ChangePassword.as_view()),
    path('forget/reset/password/', RequestPasswordRestEmail.as_view()),
    path('forget/new/password/', SetNewPasswordView.as_view()),

]