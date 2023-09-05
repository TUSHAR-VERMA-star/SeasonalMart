from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout, name="logout"),
    path('forgotPassword/', forgotPassword, name="forgotPassword"),
    path('resetPassword/', resetPassword, name="resetPassword"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
]
