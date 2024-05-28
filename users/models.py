from django.db import models
# from django.utils import timezone


class app_user_mst(models.Model):
    user_name = models.CharField(max_length=100, primary_key=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_name}'


class UserProfile(models.Model):
    user_name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(
        blank=True, null=True, default='Write your description....')
    image = models.ImageField(
        upload_to='images/', default='images/default_image.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_name} '


class LinkProfile(models.Model):
    user_name = models.CharField(max_length=100)
    channel_url = models.URLField(blank=True)
    personal_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_name}'
