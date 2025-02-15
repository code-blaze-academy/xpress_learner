from rest_framework import routers
from core_root_api.security.auth.viewsets.register import RegisterViewSet,AdminRegisterViewSet
from core_root_api.security.auth.viewsets.login import LoginViewSet,AdminLoginViewset
from core_root_api.security.auth.viewsets.forgot_password import ForgotPasswordViewset
from core_root_api.security.auth.viewsets.confirm_reset_code import ConfirmResetCodeViewset
from core_root_api.security.auth.viewsets.reset_password_change import ResetChangePasswordView
router=routers.SimpleRouter()
router.register(r'register',RegisterViewSet,basename='register')
# router.register(r'admin-board/register',AdminRegisterViewSet,basename='admin_register')

router.register(r'login',LoginViewSet,basename='login')
router.register(r'admin-board/login',AdminLoginViewset,basename='admin_login')
router.register(r'password/forgot-password',ForgotPasswordViewset,basename='forgot-password')
router.register(r"password/confirm-otp", ConfirmResetCodeViewset, basename="otp_confirm")
router.register(r'password/reset-change-password', ResetChangePasswordView, basename="reset-password-change")




urlpatterns=[
    *router.urls
]
