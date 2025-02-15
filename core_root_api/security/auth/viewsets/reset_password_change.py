from core_root_api.security.auth.serializer.reset_password_change import ResetChangePasswordSerializer
from core_root_api.security.auth.models import CodeGenerator
from rest_framework.permissions import AllowAny
from core_root_api.security.user.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from drf_yasg import openapi
from core_root_api.security.user.models import User
from core_root_api.security.auth.viewsets.password import PasswordManager

class ResetChangePasswordView(viewsets.ModelViewSet):
    
    serializer_class = ResetChangePasswordSerializer
    permission_classes = [AllowAny, ]
    http_method_names=['post']

    @swagger_auto_schema(operation_description="Reset Password")
    def create(self, request):
        serializer = ResetChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email  = serializer.validated_data.get("email")
            
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']

            if password==confirm_password:
                password_manager = PasswordManager(password).verify_password()
                if  not password_manager[0]:
                    response_data=dict()
                    # response_data = {"status": False, "error": password_manager[1].split("-")[0].replace("Issues:", "")}
                    issues = password_manager[1].split("-")[1:]
                    response_data['error'] = [value for value in issues]
                    return Response( response_data, status=status.HTTP_400_BAD_REQUEST)
                if len(password)>=8:
                    try:
                        current_user=User.objects.get(email=email)
                    except User.DoesNotExist:
                        return Response({"status":False,"error":"Password must be at least 8 characters"},status=status.HTTP_400_BAD_REQUEST)
                    current_user.set_password(password)
                
                    current_user.save()
                    return Response({"message": "Password Changed","status":True}, status=status.HTTP_200_OK)
                else:
                    
                    return Response({"error": "password must be upto 8 characters","status":False}, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Password and confirm password is not the same","status":False}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
