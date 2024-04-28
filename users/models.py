from django.db import models


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
