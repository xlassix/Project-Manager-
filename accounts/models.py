from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
import re


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True,null=False)
    username = models.CharField('username', max_length=30,unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    class Meta:
        managed=True
        db_table = 'Users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


from rest_framework import serializers
from .core import EmailBackend
from django.contrib.auth import authenticate
#password = RegexValidator('((?=.*\d)(?=.*[A-Z])(?=.*\W).{8,8})', ".")
Users=EmailBackend()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30,min_length=8, allow_blank=False)
    def validate_username(self, value):
        if Users.check_user(username=value):
            raise serializers.ValidationError("Account already exist",code="not unique")
        return value 
    def validate_password(self,value):
        if not bool(re.match(r'((?=.*\d)(?=.*[A-Z])(?=.*\W).{8,8})', value)):
            raise serializers.ValidationError(["must contain at least one digit","must contain at least one uppercase character",'must contain at least one special symbol'],code="invalid")
        """if not bool(re.match(r'(?=.*[A-Z])', value)):
            raise serializers.ValidationError("must contain at least one uppercase character",code="invalid")
        if not bool(re.match(r'(?=.*\W)', value)):
            raise serializers.ValidationError(,code='invalid')"""
        
        return value
    def create(self, validated_data):
        password = validated_data['password']
        username= validated_data["username"]
        User.objects._create_user_Api(password=password,username=username)
        user = authenticate(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return token
    class Meta:
        model = User
        fields = ['username',"password"]
        
    
