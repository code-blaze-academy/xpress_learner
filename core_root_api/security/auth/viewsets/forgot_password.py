from core_root_api.security.auth.serializer.forgot_password import ForgetPasswordSerializer
from core_root_api.security.auth.models import  CodeGenerator
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from core_root_api.security.user.models import User
from rest_framework.response import Response
from rest_framework import viewsets, status
from core_root_api.custom_api_urls import email_smtp_api_url
from django.conf import settings
import random
import requests
# from core_app_root.security.user.views import EmailUtility



class ForgotPasswordViewset(viewsets.ModelViewSet):
    
    serializer_class=ForgetPasswordSerializer
    permission_classes=[AllowAny,]
    queryset=CodeGenerator.objects.all()
    http_method_names=['post']
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"status": False, "active": False, "error": f"{email} does not exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            while True:
                activation_code = random.randint(1000, 9999)            
                codes = [i.code_authentication for i in CodeGenerator.objects.all()]
                if not activation_code in codes:
                    break
            subject = "Resetting Password Code"
            
            try:
                if code_generator := CodeGenerator.objects.filter(user=user).first():
                    code_generator.code_authentication = str(activation_code)
                    code_generator.save()
                else:
                    CodeGenerator.objects.create(user=user, code_authentication=str(activation_code))             
                # EmailUtility.send_otp_reset_email(user, activation_code)
                receiver_email = email
                subject = "Password Reset "
                message=f"""You have been sent this email because we received a
                request to reset the password to your
                Xpress learner account.<br />If you requested a
                code, please enter the
                5-digit code sent to you. Your code :  {activation_code}, If you did not request
                a code, you can safely ignore this
                message.
                """
                # body = f"Enter the four digit code sent to you here in your Blanc Exchange application to continue with account registration completion   {activation_code} , you can copy and paste the activation code"
                mail_body={
                    "userEmail":receiver_email,
                    "text":message,
                    "subject":"Password Reset",
                    "title":f"Request for Password reset"
                }
                
                response_mail=requests.post(url=f"{email_smtp_api_url}",json=mail_body)
                
                if str(response_mail.json()['msg'])=="You should receive an email from us":
                
                    return Response({"status": True, "data": serializer.data, "message": "Reset password code sent to your email"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":False,"error":"could not recieve email at the moment ,try again later"},status=status.HTTP_501_NOT_IMPLEMENTED)
            except Exception as e:
                return Response({"status": False, "error": f"Error sending email: "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

