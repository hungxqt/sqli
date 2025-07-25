from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Email(models.Model):
    email_id = models.CharField(max_length=30)

class UAgent(models.Model):
    uagent = models.CharField(max_length=256)
    ip_address = models.CharField(max_length=35)
    username = models.CharField(max_length=20)

class Referer(models.Model):
    referer = models.CharField(max_length=256)
    ip_address = models.CharField(max_length=35)
