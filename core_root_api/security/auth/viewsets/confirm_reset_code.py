from core_root_api.security.auth.serializer.confirm_reset_code import ConfirmResetCodeSerializer
from core_root_api.security.auth.models import CodeGenerator
from core_root_api.security.user.models import User
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg import openapi

class ConfirmResetCodeViewset(viewsets.ModelViewSet):
    
    serializer_class = ConfirmResetCodeSerializer
    permission_classes=[AllowAny,]
    queryset=CodeGenerator.objects.all()
    http_method_names=['post']
    
    # @action(detail=False, url_path='verify/(?P<email>[^/]+)')
    @swagger_auto_schema(operation_description="Reset Password",)
    def create(self,request):
        serializer=self.serializer_class(data=request.data)
        email = serializer.initial_data.get('email')
        print(email)
        if not email:
            return Response(
                {"is_active": False, "status": False, "error_msg": "No email query"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"status": False, "active": False, "error_msg": f"{email} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if serializer.is_valid(raise_exception=True):
                code_authentication=serializer.validated_data['code_authentication']
                try:
                    current_user=CodeGenerator.objects.get(code_authentication=code_authentication, user=user)
                    return Response({"status":True,"success_msg":f"Password reset successfully for {email}"},status=status.HTTP_200_OK)
                except CodeGenerator.DoesNotExist:
                    return Response({"status":False,"error_msg":"The code provided does not exist"})
        except Exception as e:
            return Response(
                {"status":False,"error_msg":f"Your request cant be processed now, check your network and try again. E: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    