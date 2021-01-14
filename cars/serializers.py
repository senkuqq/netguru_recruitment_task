from rest_framework import serializers, exceptions

from cars.models import Car, Make, CarRating
from cars.vpic_client import VpicClient
from rest_framework import status


class CarRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRating
        fields = ['rating']


class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.name')
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'name', 'make', 'average_rating']

    def validate(self, attrs):
        client = VpicClient()
        make_name = attrs.get('make').get('name')
        car_name = attrs.get('name')
        if client.get_car_data_by_make_and_name(make_name=make_name, car_name=car_name):
            pass
        else:
            raise exceptions.NotFound("Car and make is not present in Product Information Catalog "
                                      "and Vehicle Listing (vPIC) ", code=status.HTTP_404_NOT_FOUND)
        try:
            Car.objects.get(make__name__iexact=make_name, name__iexact=car_name)
        except Car.DoesNotExist:
            return attrs
        else:
            raise exceptions.ValidationError('Car already exists in database')

    def create(self, validated_data):
        make, created = Make.objects.get_or_create(name=validated_data.get('make').get('name').capitalize())
        return Car.objects.create(name=validated_data.get('name'),
                                  make=make)
