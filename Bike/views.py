import django
from django.http import HttpResponse
from rest_framework import viewsets

from Bike.models import Bike
from user.models import User


class BikeAPI(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            token = request.data['token']
            req = request.data['request']
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        
        try:
            user = User.objects.get(token=token)
        except:
            return HttpResponse('Token not valid', status=409)
        if not user:
            return HttpResponse('Token not valid', status=409)

        if req == 'Create':
            if not user.isAdmin:
                return HttpResponse('Unauthorized', status=401)
            try:
                bike_id = request.data.get('unique_id')
                locationX = request.data.get('locationX')
                locationY = request.data.get('locationY')
            except KeyError:
                return HttpResponse('error in fields', status=406)

            bike = Bike()
            bike.unique_id, bike.locationX, bike.locationY = bike_id, locationX, locationY

            try:
                bike.save()
            except django.db.utils.IntegrityError:
                return HttpResponse('Conflict', status=409)
            return HttpResponse('Bike created successfully', status=200)
