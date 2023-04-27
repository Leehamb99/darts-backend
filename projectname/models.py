
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
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    related_players = models.ManyToManyField('self', blank=True)

    def get_all_related_players(self):
        """
        Returns a queryset of all the related players of this DartsPlayer object,
        including indirect relations.
        """
        related_players = set()
        stack = [self]
        while stack:
            current_player = stack.pop()
            related_players.add(current_player)
        return DartsPlayer.objects.filter(id__in=[player.id for player in related_players])


    @property
    def dart_average(self):
        return(self.score / (self.darts_thrown / 3)  )


    USERNAME_FIELD = 'username'

