from rest_framework import routers
from core_root_api.security.auth.viewsets.register import RegisterViewSet,AdminRegisterViewSet
from core_root_api.security.auth.viewsets.login import LoginViewSet,AdminLoginViewset
from core_root_api.security.auth.viewsets.forgot_password import ForgotPasswordViewset
router=routers.SimpleRouter()
router.register(r'register',RegisterViewSet,basename='register')
# router.register(r'admin-board/register',AdminRegisterViewSet,basename='admin_register')

router.register(r'login',LoginViewSet,basename='login')
router.register(r'admin-board/login',AdminLoginViewset,basename='admin_login')
router.register(r'password/forgot-password',ForgotPasswordViewset,basename='forgot-password')


urlpatterns=[
    *router.urls
]
