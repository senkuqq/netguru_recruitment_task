import requests
import json
from django.conf import settings

DOMAIN = 'https://vpic.nhtsa.dot.gov/api/'
JSON_FORMAT = 'json'


class VpicClient():
    def get_cars_dataset_by_make(self, make_name):
        response = requests.get('{}/vehicles/GetModelsForMake/{}?format={}'.format(DOMAIN, make_name, JSON_FORMAT))
        return response

    def get_car_data_by_make_and_name(self, make_name, car_name):
        response = self.get_cars_dataset_by_make(make_name)
        is_in_dataset = False
        if response.status_code == 200:
            results = response.json().get('Results')
            for model in results:
                if model['Model_Name'].capitalize() == car_name.capitalize():
                    is_in_dataset = True
                    break
        return is_in_dataset
