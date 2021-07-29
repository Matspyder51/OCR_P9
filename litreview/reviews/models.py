from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Ticket(models.Model):
	title = models.CharField(max_length=128)
	description = models.TextField()
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	image = models.ImageField()
	time_created = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
	ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(validators=[
		MinValueValidator(0),
		MaxValueValidator(5)
	])
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	headline = models.CharField(max_length=128)
	body = models.TextField(max_length=8192, blank=True)
	time_created = models.DateTimeField(auto_now_add=True)