#!/usr/bin/venv python3


from rest_framework.exceptions import NotFound, ValidationError, AuthenticationFailed
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from core_root_api.security.user.models import User

from drf_yasg.utils import swagger_auto_schema
from django.utils.encoding import force_bytes
from django.templatetags.static import static
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from django.utils.html import strip_tags
from django.core import exceptions as VT
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.views import View
from drf_yasg import openapi
from django import forms
import re


token_generator = PasswordResetTokenGenerator()


class PasswordManager:
    
    def __init__(self, password):
        self.password = password

    def checking_password(self):
        criteria = {
            "length": len(self.password) >= 8,
            "uppercase": bool(re.search(r"[A-Z]", self.password)),
            "lowercase": bool(re.search(r"[a-z]", self.password)),
            "digit": bool(re.search(r"\d", self.password)),
            "special_character": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password)),
        }
        non_conformities = [key for key, valid in criteria.items() if not valid]
        if non_conformities:
            return {"is_strong": False, "non_conformities": non_conformities}
        else:
            return {"is_strong": True, "non_conformities": []}

    def verify_password(self):
        
        result = self.checking_password()

        if result["is_strong"]:
            return (True, '')
        else:
            sent = "Password is not strong. Issues:"
            for issue in result["non_conformities"]:
                sent += f" - Does not meet the {issue.replace('_', ' ')} criterion."
            return (False, sent)

