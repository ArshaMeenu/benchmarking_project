from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Footballer(models.Model):
    name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    competitions = models.ManyToManyField(to=Competition)
    age = models.IntegerField(default=18)
    season_goals = models.IntegerField(default=0)
    season_assists = models.IntegerField(default=0)

    def __str__(self):
        return self.name
