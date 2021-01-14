from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models import Avg


class Make(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100)
    make = models.ForeignKey(Make, on_delete=models.PROTECT)

    @property
    def average_rating(self):
        return self.carrating_set.aggregate(Avg('rating')).get('rating__avg')

    class Meta:
        unique_together = ('name', 'make')


class CarRating(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


