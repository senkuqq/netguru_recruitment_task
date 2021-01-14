from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from cars.models import Car, CarRating
from cars.serializers import CarSerializer, CarRateSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields = '__all__'
    ordering = ['-id']

    @action(detail=True, url_path='rate', methods=['post'], serializer_class=CarRateSerializer)
    def rate(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CarRating.objects.create(car_id=pk, rating=serializer.data.get('rating'))
        return Response(serializer.data, status='201')

    @action(detail=False, url_path='popular', methods=['get'])
    def popular(self, request):
        queryset = Car.objects.annotate(count=Count('carrating__id')).order_by('-count')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


