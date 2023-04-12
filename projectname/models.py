
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(
            username=username
        )
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)    


class DartsPlayer(AbstractBaseUser):
    objects = MyUserManager()
    class Meta:
        db_table = 'user_entity'
    id = models.AutoField(primary_key=True, db_column='userId')
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    darts_thrown = models.IntegerField(default=0)
    T20_count = models.IntegerField(default=0)

    @property
    def dart_average(self):
        return(self.score / (self.darts_thrown / 3)  )


    USERNAME_FIELD = 'username'
