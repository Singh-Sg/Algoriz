from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=200)
    pnl = models.CharField(max_length=10000)
    position = models.CharField(max_length=10000)
