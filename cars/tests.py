import json

import factory
from django.test import TestCase
from rest_framework.test import APIClient
from cars.models import Car, Make, CarRating
from cars.vpic_client import VpicClient

# Create your tests here.


class CarFactory(factory.Factory):
    class Meta:
        model = Car


class MakeFactory(factory.Factory):
    class Meta:
        model = Make


class TestCars(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.make = Make.objects.create(name='Honda')
        self.car1 = Car.objects.create(make=self.make, name='model1')
        self.car2 = Car.objects.create(make=self.make, name='model2')
        self.car3 = Car.objects.create(make=self.make, name='model3')
        CarRating.objects.create(car=self.car2, rating=3)
        CarRating.objects.create(car=self.car2, rating=3)
        CarRating.objects.create(car=self.car2, rating=3)
        self.vpic = VpicClient()

    def test_connection_vpic_client(self):
        response = self.vpic.get_cars_dataset_by_make(make_name='Honda')
        self.assertTrue(response.status_code == 200, 'Wrong status code')

    def test_get_list_of_cars(self):
        response = self.client.get('/api/v1/car/', content_type='application/json')
        results = response.json().get('results')
        self.assertTrue(response.status_code == 200, 'Wrong status code')
        self.assertTrue(len(results) == 3, 'Results should have 3 records')

    def test_get_list_of_cars_popular(self):
        response = self.client.get('/api/v1/car/popular/', content_type='application/json')
        results = response.json().get('results')
        self.assertTrue(len(results) == 3, 'Results should have 3 records!')
        self.assertTrue(results[0].get("id") == self.car2.id, 'Car2 should be the most popular!')

    def test_post_car(self):
        payload = {
            "make": "Mercedes",
            "name": "S-Class",
        }
        response = self.client.post('/api/v1/car/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(response.status_code == 201, 'Wrong status code!')
        self.assertTrue(Car.objects.filter(name='S-Class', make__name='Mercedes').exists(), 'Car not created!')

    def test_post_not_existing_car(self):
        payload = {
            "make": "MySuperCarMaker",
            "name": "SuperS",
        }
        response = self.client.post('/api/v1/car/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(response.status_code == 404, 'Wrong status code!')

    def test_post_car_rating(self):
        payload = {
            "rating": 2,
        }
        response = self.client.post('/api/v1/car/{}/rate/'.format(self.car3.id), data=json.dumps(payload), content_type='application/json')
        self.assertTrue(response.status_code == 201, 'Wrong status code!')
        self.assertTrue(CarRating.objects.filter(car=self.car3).exists(), 'Car rating not created!')