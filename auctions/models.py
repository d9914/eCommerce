from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage


class User(AbstractUser):
    pass


class Category(models.Model):
    categorgy_name = models.CharField(max_length=64)

    def __str__(self):
        return self.categorgy_name


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categorys", blank=True, null=True)

    def __str__(self):
        return self.title
