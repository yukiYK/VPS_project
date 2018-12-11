import hashlib
import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'user'

    @classmethod
    def create(cls, phone, password):
        user = User(phone=phone,
                    password=cls.__encrypt_password(password))
        user.save()
        return user

    @classmethod
    def get_by_phone(cls, phone):
        return cls.objects.filter(phone=phone).first()

    def check_password(self, password):
        """
        校验密码
        :param password:
        :return:
        """
        if self.password.find("&") > -1:
            salt, hash_val = self.password.split("&")
            return self.__hex_digest(salt, password) == hash_val
        else:
            return self.password == password

    @classmethod
    def __encrypt_password(cls, raw_password):
        """
        用sha1哈希密码
        :param str raw_password: 原始密码
        :return: 加密后的密码
        """
        raw_val = str(random.random())
        salt = cls.__hex_digest(str(raw_val), str(raw_val))[:6]
        hash_val = cls.__hex_digest(salt, raw_password)
        return "%s&%s" % (salt, hash_val)

    @staticmethod
    def __hex_digest(salt, raw):
        """
        hash加密
        :param str salt:盐
        :param str raw:原始输入
        :return: 加密后的密码字符
        """
        salt = salt.encode("utf8")
        raw = raw.encode("utf8")
        return hashlib.sha1(salt+raw+salt).hexdigest()
