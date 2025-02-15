from django.db import models
from core_root_api.security.user.models import User
class CodeGenerator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code_authentication = models.CharField(max_length=50)