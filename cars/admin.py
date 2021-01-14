from django.contrib import admin

# Register your models here.
from cars.models import CarRating, Car, Make

admin.site.register(Car)
admin.site.register(CarRating)
admin.site.register(Make)