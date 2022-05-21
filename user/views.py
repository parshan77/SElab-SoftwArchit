import datetime
import hashlib
import random
import string

import django
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from user.models import User, Ride
from Bike.models import Bike
from django.shortcuts import render
import requests

import math

from django.db.utils import OperationalError

format_list = [('', '(all)')]
geom_type_list = [('', '(all)')]
try:

    admin = User()
    admin.username = 'admin'
    admin.password = hashlib.md5('admin'.encode('utf-8')).digest()
    admin.isAdmin = True

    try:
        admin.save()
    except django.db.utils.IntegrityError:
        admin = User.objects.get(username='admin')

except OperationalError:
    pass

failed_atts = [0, 0, 0, 0]
last_month_dist = 1


def haversine_distance(lat1, lon1, lat2, lon2):
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = radius * c
    return d


class API(viewsets.ViewSet):
    def handle_request(self, request):
        print(request.data)
        try:
            service = request.data["service"]
        except KeyError:
            return HttpResponse('Bad Request', status=400)
        if service == 'register':
            if failed_atts[0] < 3:
                return self.register(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'login':
            if failed_atts[1] < 3:
                return self.login(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'start_ride':
            if failed_atts[2] < 3:
                return self.start_ride(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'finish_ride':
            if failed_atts[3] < 3:
                return self.finish_ride(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        return HttpResponse('Bad Request', status=400)

    @staticmethod
    def register(data):
        url = 'http://127.0.0.1:8000/api/register'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[0] += 1
            return HttpResponse('Service Unavailable', status=503)

        if response.status_code / 100 == 5:
            failed_atts[0] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def login(data):
        url = 'http://127.0.0.1:8000/api/login'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)

        print(response.status_code)
        if response.status_code / 100 == 5:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)

        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def start_ride(data):
        url = 'http://127.0.0.1:8000/api/start_ride'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)

        print(response.status_code)
        if response.status_code / 100 == 5:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)

        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def finish_ride(data):
        url = 'http://127.0.0.1:8000/api/finish_ride'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)

        print(response.status_code)
        if response.status_code / 100 == 5:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)

        return HttpResponse(response.text, status=response.status_code)


class Register(viewsets.ViewSet):
    def handle_request(self, request):
        user = User()
        data = request.data

        try:
            # user.email = data['email']
            user.username, user.password = data['username'], hashlib.md5(data['password'].encode('utf-8')).digest()
            user.locationX = data['locationX']
            user.locationY = data['locationY']
            try:

                user.save()
            except django.db.utils.IntegrityError:
                return HttpResponse('Conflict', status=409)
        except KeyError:
            return HttpResponse('Error in registering user.', status=406)
        return HttpResponse('User created', status=200)


class Login(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            username, password = request.data['username'], str(request.data['password'])
        except KeyError:
            return HttpResponse('Empty field', status=406)

        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse("Wrong input", status=404)

        if str(user.password) == str(hashlib.md5(password.encode('utf-8')).digest()):
            if user.token_exp_time > django.utils.timezone.now():
                return HttpResponse(user.token, status=200)
            else:
                user.token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
                user.token_exp_time = django.utils.timezone.now() + django.utils.timezone.timedelta(hours=1, minutes=30)
                user.save()
                return HttpResponse(user.token, status=200)
        else:
            return HttpResponse("Wrong info", status=404)


class StartRide(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            bike_id = request.data['unique_id']
            user_id = request.data['user_id']
        except KeyError:
            return HttpResponse('empty field', status=406)

        try:
            bike = Bike.objects.get(unique_id=bike_id)
        except:
            return HttpResponse("Wrong bike id", status=404)

        try:
            user = User.objects.get(username=user_id)
        except:
            return HttpResponse("Wrong user id", status=404)

        print(haversine_distance(user.locationX, user.locationY, bike.locationX, bike.locationY))
        if haversine_distance(user.locationX, user.locationY, bike.locationX, bike.locationY) >= 10000:
            return HttpResponse('Distance requirement not met', status=406)

        if user.busy or not bike.available:
            return HttpResponse('user or bike are busy.', status=406)

        user.busy = True
        bike.available = False
        ride = Ride(bike_id=bike.unique_id, biker_username=user.username, \
                    startX=bike.locationX, startY=bike.locationY, ongoing=True)

        user.save()
        bike.save()
        ride.save()

        return HttpResponse("ride created.", status=200)


class FinishRide(viewsets.ViewSet):

    def handle_request(self, request):
        monthly_distances = 0
        count_rides = 0

        try:
            bike_id = request.data['unique_id']
            user_id = request.data['user_id']
            endX = request.data['end_locationX']
            endY = request.data['end_locationY']
        except KeyError:
            return HttpResponse('empty field', status=406)

        try:
            bike = Bike.objects.get(unique_id=bike_id)
            user = User.objects.get(username=user_id)
            ride = Ride.objects.get(bike_id=bike_id)
        except:
            return HttpResponse("Wrong id", status=404)

        user.busy = False
        bike.available = True
        ride.ongoing = False

        ride.endX = user.locationX = bike.locationX = endX
        ride.endY = user.locationY = bike.locationY = endY

        ride_distance = haversine_distance(ride.startX, ride.startY, ride.endX, ride.endY)
        monthly_distances += ride_distance
        count_rides += 1

        user.score += math.floor(ride_distance / (last_month_dist)) ** 2 + 1

        user.save()
        bike.save()
        ride.save()

        return HttpResponse("ride finished.", status=200)

